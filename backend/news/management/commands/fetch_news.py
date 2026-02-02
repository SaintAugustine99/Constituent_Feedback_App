import os
from datetime import datetime, timezone

import requests
from django.core.management.base import BaseCommand

from news.models import NewsArticle

HEADLINES_URL = 'https://newsapi.org/v2/top-headlines'
EVERYTHING_URL = 'https://newsapi.org/v2/everything'


class Command(BaseCommand):
    help = 'Fetches top Kenyan headlines from NewsAPI.org and saves them'

    def _fetch(self, url, params):
        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            return response.json().get('articles', [])
        except requests.RequestException as e:
            self.stderr.write(self.style.WARNING(f'Request to {url} failed: {e}'))
            return []

    def handle(self, *args, **options):
        api_key = os.environ.get('NEWSAPI_KEY')
        if not api_key:
            self.stderr.write(self.style.ERROR(
                'NEWSAPI_KEY environment variable is not set. '
                'Get a free key at https://newsapi.org/register'
            ))
            return

        # Try top-headlines for Kenya first
        articles = self._fetch(HEADLINES_URL, {
            'country': 'ke',
            'pageSize': 50,
            'apiKey': api_key,
        })

        # Fallback: search "everything" for Kenya-related news
        if not articles:
            self.stdout.write('No top-headlines for Kenya, falling back to keyword search...')
            articles = self._fetch(EVERYTHING_URL, {
                'q': 'Kenya',
                'sortBy': 'publishedAt',
                'pageSize': 50,
                'apiKey': api_key,
            })

        if not articles:
            self.stdout.write(self.style.WARNING('No articles returned from NewsAPI'))
            return

        created_count = 0
        for article in articles:
            url = article.get('url')
            if not url:
                continue

            published_str = article.get('publishedAt', '')
            try:
                published_at = datetime.fromisoformat(
                    published_str.replace('Z', '+00:00')
                )
                if published_at.tzinfo is None:
                    published_at = published_at.replace(tzinfo=timezone.utc)
            except (ValueError, AttributeError):
                continue

            _, created = NewsArticle.objects.get_or_create(
                url=url,
                defaults={
                    'title': (article.get('title') or '')[:500],
                    'description': article.get('description') or '',
                    'source_name': (article.get('source', {}) or {}).get('name', 'Unknown'),
                    'image_url': article.get('urlToImage') or '',
                    'published_at': published_at,
                },
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Fetched {len(articles)} articles, saved {created_count} new'
        ))
