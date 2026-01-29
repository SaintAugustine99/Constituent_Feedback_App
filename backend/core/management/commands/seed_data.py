from django.core.management.base import BaseCommand
from locations.models import County, Constituency, Ward, Official
from facilities.models import Facility
from projects.models import Project
from legislative_tracker.models import Docket, InstrumentCategory, LegalInstrument, PublicFeedback
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Seeds initial data for Constituent OS demo'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # 1. Ensure Locations
        county, _ = County.objects.get_or_create(name='Nairobi City', defaults={'code': '047'})
        constituency, _ = Constituency.objects.get_or_create(name='Embakasi East', county=county)
        ward, _ = Ward.objects.get_or_create(name='Utawala', constituency=constituency)

        self.stdout.write(f"Location ensured: {ward}")

        # 2. Create Officials
        Official.objects.get_or_create(
            name='Hon. Patrick Karani',
            title='MCA',
            ward=ward,
            defaults={
                'phone': '+254 700 000001',
                'email': 'mca.utawala@nairobi.go.ke',
                'whatsapp_link': 'https://wa.me/254700000001'
            }
        )
        Official.objects.get_or_create(
            name='Hon. Babu Owino',
            title='MP',
            constituency=constituency,
            defaults={
                'phone': '+254 700 000002',
                'email': 'mp.embakasieast@parliament.go.ke',
                'whatsapp_link': 'https://wa.me/254700000002'
            }
        )
        self.stdout.write("Officials seeded.")

        # 3. Create Facilities
        Facility.objects.get_or_create(
            name='Utawala Social Hall',
            ward=ward,
            defaults={
                'facility_type': 'HALL',
                'capacity': 300,
                'price_per_hour': 1500.00,
                'description': 'Multipurpose hall for community meetings and weddings.'
            }
        )
        Facility.objects.get_or_create(
            name='Mihango Sports Ground',
            ward=ward,
            defaults={
                'facility_type': 'FIELD',
                'capacity': 1000,
                'price_per_hour': 500.00,
                'description': 'Public football pitch with basic amenities.'
            }
        )
        self.stdout.write("Facilities seeded.")

        # 4. Create Projects
        Project.objects.get_or_create(
            name='Utawala Ring Road Tarmacking',
            ward=ward,
            defaults={
                'description': 'Upgrading the eastern bypass link road to bitumen standards.',
                'budget_allocated': 50000000.00,
                'amount_spent': 15000000.00,
                'contractor_name': 'City Engineering Works Ltd',
                'status': 'ONGOING',
                'completion_percentage': 35,
                'start_date': timezone.now().date(),
            }
        )
        Project.objects.get_or_create(
            name='Utawala Market Shade',
            ward=ward,
            defaults={
                'description': 'Construction of a steel structures shade for fresh produce traders.',
                'budget_allocated': 8000000.00,
                'contractor_name': 'Jenga Construction',
                'status': 'PLANNING',
                'completion_percentage': 0,
            }
        )
        self.stdout.write("Projects seeded.")

        # 5. Create Dockets
        dockets_data = [
            ('National Assembly', 'NATIONAL_PARLIAMENT', 'https://www.parliament.go.ke'),
            ('Senate', 'NATIONAL_PARLIAMENT', 'https://www.parliament.go.ke'),
            ('Nairobi City County Assembly', 'COUNTY_ASSEMBLY', 'https://nairobiassembly.go.ke'),
            ('Ministry of Health', 'NATIONAL_EXECUTIVE', 'https://www.health.go.ke'),
            ('Ministry of ICT and Digital Economy', 'NATIONAL_EXECUTIVE', 'https://www.ict.go.ke'),
            ('Council of Governors', 'COUNTY_EXECUTIVE', ''),
        ]
        docket_objs = {}
        for name, level, url in dockets_data:
            obj, _ = Docket.objects.get_or_create(
                name=name,
                defaults={'level': level, 'website_url': url or ''}
            )
            docket_objs[name] = obj
        self.stdout.write("Dockets seeded.")

        # 6. Create Instrument Categories
        categories_data = [
            ('Bill', 'A proposed law presented to Parliament or County Assembly for debate.'),
            ('Policy', 'A government policy document open for public input.'),
            ('Regulation', 'Subsidiary legislation or rules made under an Act of Parliament.'),
            ('Motion', 'A formal proposal for debate and resolution in the House.'),
        ]
        cat_objs = {}
        for name, desc in categories_data:
            obj, _ = InstrumentCategory.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
            cat_objs[name] = obj
        self.stdout.write("Instrument Categories seeded.")

        # 7. Create Legal Instruments
        today = timezone.now().date()
        instruments_data = [
            {
                'title': 'The Finance Bill, 2026',
                'docket': docket_objs['National Assembly'],
                'category': cat_objs['Bill'],
                'summary_text': 'Proposes amendments to various tax laws including income tax, VAT, and excise duty. Key provisions include digital services tax adjustments and housing levy modifications.',
                'legal_text_url': 'https://www.parliament.go.ke/finance-bill-2026',
                'current_status': 'PUBLIC_PARTICIPATION',
                'published_date': today - timedelta(days=14),
                'participation_deadline': today + timedelta(days=21),
            },
            {
                'title': 'The County Governments (Revenue Raising Process) Bill, 2026',
                'docket': docket_objs['Senate'],
                'category': cat_objs['Bill'],
                'summary_text': 'Seeks to regulate the process by which county governments impose taxes, fees, and charges. Aims to protect citizens from arbitrary revenue collection.',
                'legal_text_url': 'https://www.parliament.go.ke/county-revenue-bill-2026',
                'current_status': 'PUBLIC_PARTICIPATION',
                'published_date': today - timedelta(days=7),
                'participation_deadline': today + timedelta(days=30),
            },
            {
                'title': 'Nairobi City County Zoning and Land Use Policy',
                'docket': docket_objs['Nairobi City County Assembly'],
                'category': cat_objs['Policy'],
                'summary_text': 'A comprehensive zoning policy for Nairobi that designates residential, commercial, industrial, and green zones. Affects building permits and land use across all sub-counties.',
                'legal_text_url': 'https://nairobiassembly.go.ke/zoning-policy',
                'current_status': 'PUBLIC_PARTICIPATION',
                'published_date': today - timedelta(days=10),
                'participation_deadline': today + timedelta(days=14),
            },
            {
                'title': 'The Digital Health Regulations, 2026',
                'docket': docket_objs['Ministry of Health'],
                'category': cat_objs['Regulation'],
                'summary_text': 'Regulations governing telemedicine, electronic health records, and digital health platforms. Includes data privacy provisions for patient health information.',
                'legal_text_url': 'https://www.health.go.ke/digital-health-regs',
                'current_status': 'PUBLIC_PARTICIPATION',
                'published_date': today - timedelta(days=5),
                'participation_deadline': today + timedelta(days=25),
            },
            {
                'title': 'The Data Protection (General) Regulations, 2026',
                'docket': docket_objs['Ministry of ICT and Digital Economy'],
                'category': cat_objs['Regulation'],
                'summary_text': 'Comprehensive data protection regulations under the Data Protection Act. Covers cross-border data transfers, consent requirements, and penalties for data breaches.',
                'legal_text_url': 'https://www.ict.go.ke/data-protection-regs',
                'current_status': 'GAZETTED',
                'published_date': today - timedelta(days=30),
                'participation_deadline': today - timedelta(days=5),
            },
            {
                'title': 'Motion on Universal Healthcare Coverage Implementation',
                'docket': docket_objs['National Assembly'],
                'category': cat_objs['Motion'],
                'summary_text': 'A motion urging the government to fast-track the rollout of Universal Health Coverage across all 47 counties, with specific timelines and budget allocation.',
                'legal_text_url': 'https://www.parliament.go.ke/uhc-motion',
                'current_status': 'COMMITTEE_STAGE',
                'published_date': today - timedelta(days=45),
                'participation_deadline': today - timedelta(days=15),
            },
        ]

        instrument_objs = []
        for data in instruments_data:
            obj, _ = LegalInstrument.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            instrument_objs.append(obj)
        self.stdout.write("Legal Instruments seeded.")

        # 8. Create sample PublicFeedback entries
        feedback_data = [
            {
                'instrument': instrument_objs[0],  # Finance Bill
                'full_name': 'Jane Wanjiku',
                'constituency': 'Embakasi East',
                'ward': 'Utawala',
                'position': 'OPPOSE',
                'comments': 'The proposed increase in VAT on petroleum products will raise the cost of living for ordinary Kenyans. The housing levy should be voluntary, not mandatory.',
            },
            {
                'instrument': instrument_objs[0],  # Finance Bill
                'full_name': 'John Ochieng',
                'constituency': 'Kisumu Central',
                'ward': 'Kondele',
                'position': 'AMEND',
                'comments': 'I support the digital services tax but propose that small businesses earning below KES 500,000 annually be exempted from the new provisions.',
            },
            {
                'instrument': instrument_objs[0],  # Finance Bill
                'full_name': 'Amina Hassan',
                'constituency': 'Garissa Township',
                'ward': 'Waberi',
                'position': 'SUPPORT',
                'comments': 'The allocation for ASAL counties infrastructure is a welcome move. I support the proposed road development fund allocation.',
            },
            {
                'instrument': instrument_objs[2],  # Zoning Policy
                'full_name': 'Peter Mwangi',
                'constituency': 'Embakasi East',
                'ward': 'Utawala',
                'position': 'AMEND',
                'comments': 'Utawala should be rezoned from purely residential to mixed-use to support the growing commercial activities along the Eastern Bypass.',
            },
            {
                'instrument': instrument_objs[2],  # Zoning Policy
                'full_name': 'Sarah Njeri',
                'constituency': 'Westlands',
                'ward': 'Parklands/Highridge',
                'position': 'SUPPORT',
                'comments': 'The green zone designations along Karura Forest and City Park are essential for environmental protection. Fully support this policy.',
            },
            {
                'instrument': instrument_objs[3],  # Digital Health
                'full_name': 'Dr. Kiprop Tanui',
                'constituency': 'Kapseret',
                'ward': 'Ngeria',
                'position': 'SUPPORT',
                'comments': 'Telemedicine regulations are long overdue. This will improve healthcare access in rural areas significantly.',
            },
            {
                'instrument': instrument_objs[3],  # Digital Health
                'full_name': 'Mary Akinyi',
                'constituency': 'Seme',
                'ward': 'Central Seme',
                'position': 'OPPOSE',
                'comments': 'The data privacy provisions are too weak. Patient health records need stronger encryption requirements and stricter access controls.',
            },
            {
                'instrument': instrument_objs[1],  # County Revenue Bill
                'full_name': 'Hassan Abdi',
                'constituency': 'Mandera East',
                'ward': 'Township',
                'position': 'SUPPORT',
                'comments': 'Counties must have clear guidelines on revenue collection. This bill will protect traders from being overtaxed by county governments.',
            },
        ]

        for fb in feedback_data:
            PublicFeedback.objects.get_or_create(
                instrument=fb['instrument'],
                full_name=fb['full_name'],
                defaults=fb
            )
        self.stdout.write("Public Feedback seeded.")

        self.stdout.write(self.style.SUCCESS('Successfully seeded Constituent OS data!'))
