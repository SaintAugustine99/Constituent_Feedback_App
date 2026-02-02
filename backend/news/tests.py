from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from .models import GovernmentResource, NewsArticle


class GovernmentResourceTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        GovernmentResource.objects.create(
            name='Kenya Law', url='http://kenyalaw.org',
            description='Legal resources', category='LEGAL', order=1,
        )
        GovernmentResource.objects.create(
            name='Parliament', url='http://parliament.go.ke',
            description='Legislative resources', category='LEGISLATIVE', order=2,
        )

    def test_list_resources_public(self):
        response = self.client.get('/api/news/resources/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_resource_ordering(self):
        response = self.client.get('/api/news/resources/')
        self.assertEqual(response.data[0]['name'], 'Kenya Law')

    def test_resource_str(self):
        r = GovernmentResource.objects.first()
        self.assertEqual(str(r), 'Kenya Law')


class NewsArticleTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.article = NewsArticle.objects.create(
            title='New Bill Introduced',
            description='A new bill was introduced today.',
            source_name='Daily Nation',
            url='http://example.com/article1',
            published_at=timezone.now(),
        )

    def test_list_articles_public(self):
        response = self.client.get('/api/news/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_article_has_time_ago_field(self):
        response = self.client.get('/api/news/articles/')
        self.assertIn('time_ago', response.data[0])
        self.assertIn('ago', response.data[0]['time_ago'])

    def test_article_str(self):
        self.assertEqual(str(self.article), 'New Bill Introduced')
