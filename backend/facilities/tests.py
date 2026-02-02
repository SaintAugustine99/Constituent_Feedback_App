from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from locations.models import County, Constituency, Ward
from accounts.models import User
from .models import Facility, Booking


class BookingModelTests(TestCase):

    def setUp(self):
        county = County.objects.create(name='Nairobi', code='047')
        constituency = Constituency.objects.create(name='Westlands', county=county)
        self.ward = Ward.objects.create(name='Parklands', constituency=constituency)
        self.user = User.objects.create_user(username='booker', password='StrongPass123!')
        self.facility = Facility.objects.create(
            name='Community Hall', facility_type='HALL',
            ward=self.ward, capacity=100,
        )
        self.base_time = timezone.now() + timedelta(days=1)

    def test_valid_booking_saves(self):
        booking = Booking(
            user=self.user, facility=self.facility,
            start_time=self.base_time,
            end_time=self.base_time + timedelta(hours=2),
            purpose='Meeting',
        )
        booking.save()
        self.assertEqual(Booking.objects.count(), 1)

    def test_end_before_start_raises_error(self):
        booking = Booking(
            user=self.user, facility=self.facility,
            start_time=self.base_time,
            end_time=self.base_time - timedelta(hours=1),
            purpose='Bad booking',
        )
        with self.assertRaises(ValidationError):
            booking.clean()

    def test_end_equals_start_raises_error(self):
        booking = Booking(
            user=self.user, facility=self.facility,
            start_time=self.base_time,
            end_time=self.base_time,
            purpose='Zero duration',
        )
        with self.assertRaises(ValidationError):
            booking.clean()

    def test_overlapping_booking_raises_error(self):
        Booking.objects.create(
            user=self.user, facility=self.facility,
            start_time=self.base_time,
            end_time=self.base_time + timedelta(hours=2),
            purpose='First booking', status='CONFIRMED',
        )
        overlapping = Booking(
            user=self.user, facility=self.facility,
            start_time=self.base_time + timedelta(hours=1),
            end_time=self.base_time + timedelta(hours=3),
            purpose='Overlapping',
        )
        with self.assertRaises(ValidationError):
            overlapping.clean()

    def test_non_overlapping_booking_succeeds(self):
        Booking.objects.create(
            user=self.user, facility=self.facility,
            start_time=self.base_time,
            end_time=self.base_time + timedelta(hours=2),
            purpose='First', status='CONFIRMED',
        )
        non_overlapping = Booking(
            user=self.user, facility=self.facility,
            start_time=self.base_time + timedelta(hours=3),
            end_time=self.base_time + timedelta(hours=5),
            purpose='Later booking',
        )
        non_overlapping.save()
        self.assertEqual(Booking.objects.count(), 2)

    def test_cancelled_booking_does_not_block(self):
        Booking.objects.create(
            user=self.user, facility=self.facility,
            start_time=self.base_time,
            end_time=self.base_time + timedelta(hours=2),
            purpose='Cancelled', status='CANCELLED',
        )
        new_booking = Booking(
            user=self.user, facility=self.facility,
            start_time=self.base_time,
            end_time=self.base_time + timedelta(hours=2),
            purpose='Replacement',
        )
        new_booking.save()
        self.assertEqual(Booking.objects.count(), 2)

    def test_facility_str(self):
        self.assertEqual(str(self.facility), 'Community Hall (Social Hall) - Parklands')


class FacilityAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        county = County.objects.create(name='Nairobi', code='047')
        constituency = Constituency.objects.create(name='Westlands', county=county)
        self.ward = Ward.objects.create(name='Parklands', constituency=constituency)
        self.facility = Facility.objects.create(
            name='Sports Ground', facility_type='FIELD',
            ward=self.ward, capacity=500,
        )
        self.user = User.objects.create_user(username='booker', password='StrongPass123!')
        self.token = Token.objects.create(user=self.user)

    def test_list_facilities_public(self):
        response = self.client.get('/api/facilities/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_booking_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        base = timezone.now() + timedelta(days=2)
        data = {
            'facility': self.facility.id,
            'start_time': base.isoformat(),
            'end_time': (base + timedelta(hours=2)).isoformat(),
            'purpose': 'Football match',
        }
        response = self.client.post('/api/facilities/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.first().user, self.user)

    def test_create_booking_unauthenticated(self):
        base = timezone.now() + timedelta(days=2)
        data = {
            'facility': self.facility.id,
            'start_time': base.isoformat(),
            'end_time': (base + timedelta(hours=2)).isoformat(),
            'purpose': 'Event',
        }
        response = self.client.post('/api/facilities/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_sees_only_own_bookings(self):
        other = User.objects.create_user(username='other', password='StrongPass123!')
        base = timezone.now() + timedelta(days=3)
        Booking.objects.create(
            user=self.user, facility=self.facility,
            start_time=base, end_time=base + timedelta(hours=1),
            purpose='Mine',
        )
        Booking.objects.create(
            user=other, facility=self.facility,
            start_time=base + timedelta(hours=2), end_time=base + timedelta(hours=3),
            purpose='Theirs',
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/facilities/bookings/')
        self.assertEqual(len(response.data), 1)
