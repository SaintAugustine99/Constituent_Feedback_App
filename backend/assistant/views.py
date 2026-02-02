import os
import logging

from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

import google.generativeai as genai

from legislative_tracker.models import LegalInstrument, PublicFeedback

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

SYSTEM_PROMPT = """You are **Jamii Assistant**, a friendly and knowledgeable Kenyan civic engagement advisor built into the Jamii Platform.

Your role:
- Explain Kenyan legislation, bills, and policies in simple language.
- Guide citizens on how to submit feedback on active bills.
- Summarise public sentiment when feedback data is provided.
- Reference government resources and civic participation rights under the Constitution of Kenya 2010.
- Encourage constructive civic participation.

Rules:
- Be concise and helpful. Use plain language accessible to all Kenyans.
- When you have context about a specific bill, reference it directly.
- If you don't know something, say so honestly rather than guessing.
- Never give legal advice — suggest consulting a qualified advocate for legal matters.
- Keep responses focused on civic participation and governance.
"""

RESOURCE_LINKS = """
Useful Government Resources:
- Kenya Law: http://kenyalaw.org
- Parliament of Kenya: http://parliament.go.ke
- County Assembly Forum: http://caf.go.ke
- IEBC: https://www.iebc.or.ke
- Constitution of Kenya 2010: http://kenyalaw.org/kl/index.php?id=398
"""


def build_context(instrument_id=None, user=None):
    """Build context sections from the database to enrich the AI prompt."""
    sections = []
    had_user_context = False
    resolved_instrument_id = None

    # User location context
    if user and user.is_authenticated:
        had_user_context = True
        ward = getattr(user, 'ward', None)
        if ward:
            constituency = ward.constituency
            county = constituency.county
            sections.append(
                f"[User Location]\n"
                f"Ward: {ward.name}, Constituency: {constituency.name}, County: {county.name}"
            )

    # Specific instrument context
    if instrument_id:
        try:
            instrument = LegalInstrument.objects.select_related(
                'docket', 'category'
            ).get(pk=instrument_id)
            resolved_instrument_id = instrument.id

            # Feedback stats
            feedback_qs = instrument.feedback.all()
            total = feedback_qs.count()
            positions = feedback_qs.values('position').annotate(count=Count('id'))
            position_counts = {p['position']: p['count'] for p in positions}

            sections.append(
                f"[Active Bill Context]\n"
                f"Title: {instrument.title}\n"
                f"Docket: {instrument.docket.name} ({instrument.docket.get_level_display()})\n"
                f"Category: {instrument.category.name}\n"
                f"Status: {instrument.get_current_status_display()}\n"
                f"Participation Deadline: {instrument.participation_deadline}\n"
                f"Open for feedback: {'Yes' if instrument.is_open() else 'No'}\n"
                f"Summary: {instrument.summary_text[:500] if instrument.summary_text else 'N/A'}\n"
                f"\nFeedback Stats — Total: {total}, "
                f"Support: {position_counts.get('SUPPORT', 0)}, "
                f"Oppose: {position_counts.get('OPPOSE', 0)}, "
                f"Amend: {position_counts.get('AMEND', 0)}"
            )

            # Recent comments (5 most recent)
            recent = feedback_qs.order_by('-submitted_at')[:5]
            if recent.exists():
                comments_text = "\n".join(
                    f"- [{fb.position}] {fb.comments[:150]}"
                    for fb in recent
                )
                sections.append(f"[Recent Public Comments]\n{comments_text}")

        except LegalInstrument.DoesNotExist:
            pass

    # Active instruments overview (always include)
    active_instruments = [
        i for i in LegalInstrument.objects.select_related('docket', 'category')
        .order_by('-created_at')[:20]
        if i.is_open()
    ][:5]

    if active_instruments:
        lines = []
        for inst in active_instruments:
            lines.append(
                f"- {inst.title} (by {inst.docket.name}) — "
                f"Deadline: {inst.participation_deadline}"
            )
        sections.append(f"[Currently Active Bills/Policies]\n" + "\n".join(lines))

    # Always include resource links
    sections.append(RESOURCE_LINKS)

    context_block = "\n\n".join(sections)
    return context_block, resolved_instrument_id, had_user_context


class AssistantChatView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        message = request.data.get('message', '').strip()
        if not message:
            return Response(
                {'error': 'Message is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        instrument_id = request.data.get('instrument_id')

        # Build context from DB
        user = request.user if request.user.is_authenticated else None
        context_block, resolved_instrument_id, had_user_context = build_context(
            instrument_id=instrument_id,
            user=user,
        )

        # Assemble full prompt
        full_system = SYSTEM_PROMPT + "\n\n--- CONTEXT ---\n" + context_block

        if not GEMINI_API_KEY:
            return Response(
                {'error': 'AI service is not configured. Please set GEMINI_API_KEY.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel(
                model_name='gemini-2.0-flash',
                system_instruction=full_system,
            )
            response = model.generate_content(message)
            reply = response.text
        except Exception as e:
            logger.exception("Gemini API call failed")
            return Response(
                {'error': f'AI service error: {str(e)}'},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response({
            'reply': reply,
            'context_used': {
                'instrument_id': resolved_instrument_id,
                'had_user_context': had_user_context,
            },
        })
