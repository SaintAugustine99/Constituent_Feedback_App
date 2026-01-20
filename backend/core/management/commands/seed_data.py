from django.core.management.base import BaseCommand
from locations.models import County, Constituency, Ward, Official
from facilities.models import Facility
from projects.models import Project
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Seeds initial data for Constituent OS demo'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # 1. Ensure Locations
        county, _ = County.objects.get_or_create(name='Nairobi', code='047')
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
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded Constituent OS data!'))
