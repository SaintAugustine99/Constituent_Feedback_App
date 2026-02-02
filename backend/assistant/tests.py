from datetime import timedelta
from unittest.mock import patch, MagicMock
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from locations.models import County, Constituency, Ward
from accounts.models import User
from legislative_tracker.models import Docket, InstrumentCategory, LegalInstrument, PublicFeedback
from .views import build_context


class BuildContextTests(TestCase):
    """Tests for the build_context function that assembles AI prompt context."""

    def setUp(self):
        self.county = County.objects.create(name='Nairobi', code='047')
        self.constituency = Constituency.objects.create(name='Westlands', county=self.county)
        self.ward = Ward.objects.create(name='Parklands', constituency=self.constituency)
        self.docket = Docket.objects.create(name='Ministry of Finance', level='NATIONAL_EXECUTIVE')
        self.category = InstrumentCategory.objects.create(name='Finance Bill')
        self.instrument = LegalInstrument.objects.create(
            title='The Finance Bill 2026',
            docket=self.docket,
            category=self.category,
            participation_deadline=timezone.now().date() + timedelta(days=30),
            legal_text_url='http://example.com/bill.pdf',
            summary_text='A bill about government revenue and taxation.',
            current_status='PUBLIC_PARTICIPATION',
        )

    def test_no_args_returns_resource_links(self):
        context, inst_id, had_user = build_context()
        self.assertIsNone(inst_id)
        self.assertFalse(had_user)
        self.assertIn('Kenya Law', context)

    def test_active_instruments_included(self):
        context, _, _ = build_context()
        self.assertIn('The Finance Bill 2026', context)
        self.assertIn('Currently Active Bills', context)

    def test_instrument_id_includes_bill_details(self):
        context, inst_id, _ = build_context(instrument_id=self.instrument.id)
        self.assertEqual(inst_id, self.instrument.id)
        self.assertIn('The Finance Bill 2026', context)
        self.assertIn('Ministry of Finance', context)
        self.assertIn('Active Bill Context', context)
        self.assertIn('Feedback Stats', context)

    def test_invalid_instrument_id_handled_gracefully(self):
        context, inst_id, _ = build_context(instrument_id=99999)
        self.assertIsNone(inst_id)
        self.assertIn('Kenya Law', context)  # still returns base context

    def test_authenticated_user_with_ward(self):
        user = User.objects.create_user(username='voter', password='StrongPass123!', ward=self.ward)
        context, _, had_user = build_context(user=user)
        self.assertTrue(had_user)
        self.assertIn('Parklands', context)
        self.assertIn('Westlands', context)
        self.assertIn('Nairobi', context)

    def test_authenticated_user_without_ward(self):
        user = User.objects.create_user(username='noward', password='StrongPass123!')
        context, _, had_user = build_context(user=user)
        self.assertTrue(had_user)
        self.assertNotIn('User Location', context)

    def test_feedback_stats_in_context(self):
        PublicFeedback.objects.create(
            instrument=self.instrument, full_name='A', position='SUPPORT', comments='Yes',
        )
        PublicFeedback.objects.create(
            instrument=self.instrument, full_name='B', position='OPPOSE', comments='No',
        )
        context, _, _ = build_context(instrument_id=self.instrument.id)
        self.assertIn('Support: 1', context)
        self.assertIn('Oppose: 1', context)

    def test_recent_comments_in_context(self):
        PublicFeedback.objects.create(
            instrument=self.instrument, full_name='Commenter',
            position='SUPPORT', comments='This bill will help farmers.',
        )
        context, _, _ = build_context(instrument_id=self.instrument.id)
        self.assertIn('Recent Public Comments', context)
        self.assertIn('This bill will help farmers', context)

    def test_max_five_active_instruments(self):
        for i in range(10):
            LegalInstrument.objects.create(
                title=f'Bill {i}', docket=self.docket, category=self.category,
                participation_deadline=timezone.now().date() + timedelta(days=30),
                legal_text_url='http://example.com/b.pdf', summary_text='...',
                current_status='PUBLIC_PARTICIPATION',
            )
        context, _, _ = build_context()
        # Count occurrences of bill lines in active section (each line starts with "- ")
        active_section = context.split('[Currently Active Bills/Policies]')[-1].split('\n\n')[0]
        bill_lines = [l for l in active_section.strip().split('\n') if l.startswith('- ')]
        self.assertLessEqual(len(bill_lines), 5)


class AssistantChatViewTests(TestCase):
    """Tests for the POST /api/assistant/chat/ endpoint."""

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/assistant/chat/'
        self.county = County.objects.create(name='Nairobi', code='047')
        self.constituency = Constituency.objects.create(name='Westlands', county=self.county)
        self.ward = Ward.objects.create(name='Parklands', constituency=self.constituency)
        self.docket = Docket.objects.create(name='Ministry of Finance', level='NATIONAL_EXECUTIVE')
        self.category = InstrumentCategory.objects.create(name='Finance Bill')
        self.instrument = LegalInstrument.objects.create(
            title='The Finance Bill 2026',
            docket=self.docket, category=self.category,
            participation_deadline=timezone.now().date() + timedelta(days=30),
            legal_text_url='http://example.com/bill.pdf', summary_text='About finance.',
            current_status='PUBLIC_PARTICIPATION',
        )

    def test_empty_message_returns_400(self):
        response = self.client.post(self.url, {'message': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_missing_message_returns_400(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('assistant.views.GEMINI_API_KEY', '')
    def test_no_api_key_returns_503(self):
        response = self.client.post(self.url, {'message': 'Hello'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

    @patch('assistant.views.GEMINI_API_KEY', 'fake-key')
    @patch('assistant.views.genai')
    def test_successful_chat(self, mock_genai):
        mock_model = MagicMock()
        mock_model.generate_content.return_value = MagicMock(text='Hello from Jamii Assistant!')
        mock_genai.GenerativeModel.return_value = mock_model

        response = self.client.post(self.url, {'message': 'What bills are open?'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reply'], 'Hello from Jamii Assistant!')
        self.assertIn('context_used', response.data)

    @patch('assistant.views.GEMINI_API_KEY', 'fake-key')
    @patch('assistant.views.genai')
    def test_chat_with_instrument_id(self, mock_genai):
        mock_model = MagicMock()
        mock_model.generate_content.return_value = MagicMock(text='Info about the bill.')
        mock_genai.GenerativeModel.return_value = mock_model

        response = self.client.post(
            self.url,
            {'message': 'Tell me about this bill', 'instrument_id': self.instrument.id},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['context_used']['instrument_id'], self.instrument.id)

    @patch('assistant.views.GEMINI_API_KEY', 'fake-key')
    @patch('assistant.views.genai')
    def test_chat_with_authenticated_user(self, mock_genai):
        mock_model = MagicMock()
        mock_model.generate_content.return_value = MagicMock(text='Hello citizen!')
        mock_genai.GenerativeModel.return_value = mock_model

        user = User.objects.create_user(username='voter', password='StrongPass123!', ward=self.ward)
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.post(self.url, {'message': 'Hello'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['context_used']['had_user_context'])

    @patch('assistant.views.GEMINI_API_KEY', 'fake-key')
    @patch('assistant.views.genai')
    def test_gemini_error_returns_502(self, mock_genai):
        mock_genai.GenerativeModel.side_effect = Exception('API quota exceeded')

        response = self.client.post(self.url, {'message': 'Hello'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)
        self.assertIn('AI service error', response.data['error'])

    @patch('assistant.views.GEMINI_API_KEY', '')
    def test_allows_any_permission(self):
        # Unauthenticated users should reach the view (not get 401)
        # They'll get 503 if no key, but NOT 401
        response = self.client.post(self.url, {'message': 'Hi'}, format='json')
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
