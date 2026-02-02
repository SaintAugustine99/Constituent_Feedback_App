from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from locations.models import County, Constituency, Ward
from accounts.models import User


class TestHelperMixin:
    """Shared setup for creating location hierarchy and users."""

    def create_location_hierarchy(self):
        self.county = County.objects.create(name='Nairobi', code='047')
        self.constituency = Constituency.objects.create(name='Westlands', county=self.county)
        self.ward = Ward.objects.create(name='Parklands', constituency=self.constituency)

    def create_user(self, username='testuser', password='StrongPass123!', ward=None):
        user = User.objects.create_user(
            username=username,
            email=f'{username}@test.com',
            password=password,
            ward=ward,
        )
        return user


class RegisterViewTests(TestHelperMixin, TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')
        self.create_location_hierarchy()

    def test_register_valid_user(self):
        data = {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'StrongPass123!',
            'phone_number': '0712345678',
            'ward_id': self.ward.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_assigns_ward(self):
        data = {
            'username': 'warduser',
            'email': 'ward@test.com',
            'password': 'StrongPass123!',
            'phone_number': '0712345678',
            'ward_id': self.ward.id,
        }
        self.client.post(self.url, data, format='json')
        user = User.objects.get(username='warduser')
        self.assertEqual(user.ward, self.ward)

    def test_register_invalid_ward_id(self):
        data = {
            'username': 'badward',
            'email': 'bad@test.com',
            'password': 'StrongPass123!',
            'ward_id': 99999,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_weak_password(self):
        data = {
            'username': 'weakpw',
            'email': 'weak@test.com',
            'password': '123',
            'ward_id': self.ward.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username(self):
        self.create_user(username='dupe')
        data = {
            'username': 'dupe',
            'email': 'dupe2@test.com',
            'password': 'StrongPass123!',
            'ward_id': self.ward.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_hashes_password(self):
        data = {
            'username': 'hashcheck',
            'email': 'hash@test.com',
            'password': 'StrongPass123!',
            'ward_id': self.ward.id,
        }
        self.client.post(self.url, data, format='json')
        user = User.objects.get(username='hashcheck')
        self.assertNotEqual(user.password, 'StrongPass123!')
        self.assertTrue(user.check_password('StrongPass123!'))


class LoginViewTests(TestHelperMixin, TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('login')
        self.create_location_hierarchy()
        self.user = self.create_user(ward=self.ward)

    def test_login_valid_credentials(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'StrongPass123!'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'testuser')

    def test_login_returns_ward_name(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'StrongPass123!'}, format='json')
        self.assertEqual(response.data['ward'], 'Parklands')

    def test_login_user_without_ward(self):
        no_ward_user = self.create_user(username='noward', ward=None)
        response = self.client.post(self.url, {'username': 'noward', 'password': 'StrongPass123!'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data['ward'])

    def test_login_invalid_credentials(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'wrong'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_login_creates_token(self):
        self.client.post(self.url, {'username': 'testuser', 'password': 'StrongPass123!'}, format='json')
        self.assertTrue(Token.objects.filter(user=self.user).exists())

    def test_login_returns_same_token_on_repeat(self):
        r1 = self.client.post(self.url, {'username': 'testuser', 'password': 'StrongPass123!'}, format='json')
        r2 = self.client.post(self.url, {'username': 'testuser', 'password': 'StrongPass123!'}, format='json')
        self.assertEqual(r1.data['token'], r2.data['token'])
