from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from locations.models import County, Constituency, Ward
from accounts.models import User
from .models import ServiceRequest


class ServiceRequestTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        county = County.objects.create(name='Nairobi', code='047')
        constituency = Constituency.objects.create(name='Westlands', county=county)
        ward = Ward.objects.create(name='Parklands', constituency=constituency)
        self.user = User.objects.create_user(
            username='citizen', password='StrongPass123!', ward=ward,
        )
        self.other_user = User.objects.create_user(
            username='other', password='StrongPass123!',
        )
        self.token = Token.objects.create(user=self.user)

    def authenticate(self, user=None, token=None):
        if token is None:
            token = self.token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_create_service_request(self):
        self.authenticate()
        data = {
            'category': 'ROAD',
            'description': 'Pothole on main street',
            'location_description': 'Near Main Market',
        }
        response = self.client.post('/api/issues/requests/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ServiceRequest.objects.count(), 1)
        self.assertEqual(ServiceRequest.objects.first().user, self.user)

    def test_unauthenticated_cannot_create(self):
        data = {
            'category': 'WATER',
            'description': 'No water supply',
        }
        response = self.client.post('/api/issues/requests/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_sees_only_own_requests(self):
        self.authenticate()
        ServiceRequest.objects.create(user=self.user, category='ROAD', description='My issue')
        ServiceRequest.objects.create(user=self.other_user, category='WATER', description='Their issue')
        response = self.client.get('/api/issues/requests/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['description'], 'My issue')

    def test_default_status_is_reported(self):
        self.authenticate()
        data = {'category': 'POWER', 'description': 'Power outage'}
        self.client.post('/api/issues/requests/', data, format='multipart')
        req = ServiceRequest.objects.first()
        self.assertEqual(req.status, 'REPORTED')

    def test_service_request_str(self):
        req = ServiceRequest.objects.create(user=self.user, category='ROAD', description='Test')
        self.assertIn('Roads & Transport', str(req))
