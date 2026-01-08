from django.core.management.base import BaseCommand
from legislative_tracker.models import Docket, InstrumentCategory, LegalInstrument
from django.utils import timezone
import datetime

class Command(BaseCommand):
    help = 'Seeds the database with sample Legislative Data'

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Seeding Legislative Data...")

        # 1. Create Dockets
        dockets = [
            {"name": "National Assembly", "level": "NATIONAL_PARLIAMENT"},
            {"name": "Senate", "level": "NATIONAL_PARLIAMENT"},
            {"name": "Nairobi City County Assembly", "level": "COUNTY_ASSEMBLY"},
            {"name": "Ministry of Health", "level": "NATIONAL_EXECUTIVE"},
        ]
        
        created_dockets = {}
        for d in dockets:
            obj, created = Docket.objects.get_or_create(name=d["name"], defaults={"level": d["level"]})
            created_dockets[d["name"]] = obj
            if created:
                self.stdout.write(f"   Created Docket: {d['name']}")

        # 2. Create Categories
        categories = ["Bill", "Policy", "Regulation", "Motion"]
        created_cats = {}
        for c in categories:
            obj, created = InstrumentCategory.objects.get_or_create(name=c, defaults={"description": f"A {c} for debate"})
            created_cats[c] = obj

        # 3. Create Legal Instruments
        instruments = [
            {
                "title": "The Finance Bill 2026",
                "docket": created_dockets["National Assembly"],
                "category": created_cats["Bill"],
                "status": "PUBLIC_PARTICIPATION",
                "days_deadline": 14,
                "summary": "A Bill to amend the laws relating to various taxes and duties."
            },
            {
                "title": "Nairobi County Zoning Policy 2026",
                "docket": created_dockets["Nairobi City County Assembly"],
                "category": created_cats["Policy"],
                "status": "PUBLIC_PARTICIPATION",
                "days_deadline": 30,
                "summary": "A policy framework for land use and urban planning in Nairobi City."
            },
            {
                "title": "Digital Health Regulations 2026",
                "docket": created_dockets["Ministry of Health"],
                "category": created_cats["Regulation"],
                "status": "DRAFT",
                "days_deadline": 60,
                "summary": "Regulations governing the use of AI in healthcare."
            }
        ]

        for i in instruments:
            deadline = timezone.now().date() + datetime.timedelta(days=i["days_deadline"])
            existing = LegalInstrument.objects.filter(title=i["title"]).exists()
            if not existing:
                LegalInstrument.objects.create(
                    title=i["title"],
                    docket=i["docket"],
                    category=i["category"],
                    current_status=i["status"],
                    participation_deadline=deadline,
                    summary_text=i["summary"],
                    legal_text_url="http://kenyalaw.org/kl/fileadmin/pdfdownloads/bills/2024/TheFinanceBill_2024.pdf"
                )
                self.stdout.write(f"   Created Instrument: {i['title']}")

        self.stdout.write("✅ Legislation Data Seeding Complete!")
