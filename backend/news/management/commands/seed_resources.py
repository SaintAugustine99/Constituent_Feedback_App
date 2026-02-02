from django.core.management.base import BaseCommand
from news.models import GovernmentResource


RESOURCES = [
    {
        'name': 'Kenya Gazette',
        'url': 'https://www.kenyagazette.co.ke/',
        'description': 'Official government publication for legal notices, appointments, and legislative supplements.',
        'category': 'LEGAL',
        'order': 1,
    },
    {
        'name': 'Kenya Law',
        'url': 'http://www.kenyalaw.org/',
        'description': 'Access all Kenyan legislation, case law, and legal resources.',
        'category': 'LEGAL',
        'order': 2,
    },
    {
        'name': 'National Council for Law Reporting',
        'url': 'http://www.kenyalaw.org/kl/',
        'description': 'Official law reports and legislative supplements.',
        'category': 'LEGAL',
        'order': 3,
    },
    {
        'name': 'Parliament of Kenya',
        'url': 'http://www.parliament.go.ke/',
        'description': 'Official site for the National Assembly and Senate proceedings.',
        'category': 'LEGISLATIVE',
        'order': 4,
    },
    {
        'name': 'Hansard - Parliamentary Debates',
        'url': 'http://www.parliament.go.ke/the-national-assembly/house-business/hansard',
        'description': 'Official records of parliamentary debates and proceedings.',
        'category': 'LEGISLATIVE',
        'order': 5,
    },
    {
        'name': 'Senate of Kenya',
        'url': 'http://www.senate.go.ke/',
        'description': 'Senate proceedings, committees, and county oversight.',
        'category': 'LEGISLATIVE',
        'order': 6,
    },
    {
        'name': 'IEBC - Electoral Commission',
        'url': 'https://www.iebc.or.ke/',
        'description': 'Independent Electoral and Boundaries Commission - voter registration and election info.',
        'category': 'ELECTORAL',
        'order': 7,
    },
    {
        'name': 'Kenya National Bureau of Statistics',
        'url': 'https://www.knbs.or.ke/',
        'description': 'National statistics, census data, and economic surveys.',
        'category': 'DATA',
        'order': 8,
    },
    {
        'name': 'eCitizen Portal',
        'url': 'https://www.ecitizen.go.ke/',
        'description': 'Access government services online - permits, certificates, and applications.',
        'category': 'SERVICES',
        'order': 9,
    },
    {
        'name': 'County Governments Portal',
        'url': 'https://www.cog.go.ke/',
        'description': 'Council of Governors - county government coordination and resources.',
        'category': 'SERVICES',
        'order': 10,
    },
]


class Command(BaseCommand):
    help = 'Seeds the database with curated Kenyan government resource links'

    def handle(self, *args, **options):
        created_count = 0
        for data in RESOURCES:
            _, created = GovernmentResource.objects.get_or_create(
                url=data['url'],
                defaults=data,
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seeded {created_count} new resources ({len(RESOURCES) - created_count} already existed)'
        ))
