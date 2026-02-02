from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from locations.models import County, Constituency, Ward
from accounts.models import User
from .models import Docket, InstrumentCategory, LegalInstrument, PublicFeedback


class TestHelperMixin:

    def create_location_hierarchy(self):
        self.county = County.objects.create(name='Nairobi', code='047')
        self.constituency = Constituency.objects.create(name='Westlands', county=self.county)
        self.ward = Ward.objects.create(name='Parklands', constituency=self.constituency)

    def create_docket_and_category(self):
        self.docket = Docket.objects.create(name='Ministry of Finance', level='NATIONAL_EXECUTIVE')
        self.category = InstrumentCategory.objects.create(name='Finance Bill')

    def create_instrument(self, title='The Finance Bill 2026', current_status='PUBLIC_PARTICIPATION',
                          deadline_offset_days=30):
        return LegalInstrument.objects.create(
            title=title,
            docket=self.docket,
            category=self.category,
            participation_deadline=timezone.now().date() + timedelta(days=deadline_offset_days),
            legal_text_url='http://example.com/bill.pdf',
            summary_text='A bill about finance.',
            current_status=current_status,
        )


class LegalInstrumentModelTests(TestHelperMixin, TestCase):

    def setUp(self):
        self.create_docket_and_category()

    def test_is_open_true_when_public_participation_and_future_deadline(self):
        instrument = self.create_instrument()
        self.assertTrue(instrument.is_open())

    def test_is_open_true_when_deadline_is_today(self):
        instrument = self.create_instrument(deadline_offset_days=0)
        self.assertTrue(instrument.is_open())

    def test_is_open_false_when_deadline_passed(self):
        instrument = self.create_instrument(deadline_offset_days=-1)
        self.assertFalse(instrument.is_open())

    def test_is_open_false_when_wrong_status(self):
        instrument = self.create_instrument(current_status='DRAFT')
        self.assertFalse(instrument.is_open())

    def test_is_open_false_when_passed_status(self):
        instrument = self.create_instrument(current_status='PASSED')
        self.assertFalse(instrument.is_open())

    def test_str(self):
        instrument = self.create_instrument()
        self.assertEqual(str(instrument), 'The Finance Bill 2026')


class DocketModelTests(TestCase):

    def test_str(self):
        docket = Docket.objects.create(name='Ministry of Health', level='NATIONAL_EXECUTIVE')
        self.assertEqual(str(docket), 'Ministry of Health (National Executive (Ministries))')


class LegalInstrumentAPITests(TestHelperMixin, TestCase):

    def setUp(self):
        self.client = APIClient()
        self.create_docket_and_category()

    def test_list_instruments(self):
        self.create_instrument()
        response = self.client.get('/api/legislation/instruments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_active_endpoint_returns_only_open(self):
        self.create_instrument(title='Open Bill')
        self.create_instrument(title='Closed Bill', current_status='PASSED')
        self.create_instrument(title='Expired Bill', deadline_offset_days=-5)
        response = self.client.get('/api/legislation/instruments/active/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [i['title'] for i in response.data]
        self.assertIn('Open Bill', titles)
        self.assertNotIn('Closed Bill', titles)
        self.assertNotIn('Expired Bill', titles)

    def test_retrieve_instrument_detail(self):
        instrument = self.create_instrument()
        response = self.client.get(f'/api/legislation/instruments/{instrument.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The Finance Bill 2026')

    def test_stats_endpoint_no_feedback(self):
        instrument = self.create_instrument()
        response = self.client.get(f'/api/legislation/instruments/{instrument.id}/stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_feedback'], 0)
        self.assertEqual(response.data['positions']['SUPPORT'], 0)

    def test_stats_endpoint_with_feedback(self):
        instrument = self.create_instrument()
        PublicFeedback.objects.create(
            instrument=instrument, full_name='Alice', position='SUPPORT', comments='Good bill',
        )
        PublicFeedback.objects.create(
            instrument=instrument, full_name='Bob', position='OPPOSE', comments='Bad bill',
        )
        PublicFeedback.objects.create(
            instrument=instrument, full_name='Carol', position='SUPPORT', comments='Great idea',
        )
        response = self.client.get(f'/api/legislation/instruments/{instrument.id}/stats/')
        self.assertEqual(response.data['total_feedback'], 3)
        self.assertEqual(response.data['positions']['SUPPORT'], 2)
        self.assertEqual(response.data['positions']['OPPOSE'], 1)
        self.assertEqual(response.data['positions']['AMEND'], 0)

    def test_search_instruments(self):
        self.create_instrument(title='The Health Bill 2026')
        self.create_instrument(title='The Finance Bill 2026')
        response = self.client.get('/api/legislation/instruments/?search=Health')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FeedbackAPITests(TestHelperMixin, TestCase):

    def setUp(self):
        self.client = APIClient()
        self.create_location_hierarchy()
        self.create_docket_and_category()
        self.instrument = self.create_instrument()

    def test_submit_feedback_as_guest(self):
        data = {
            'instrument': self.instrument.id,
            'full_name': 'Guest User',
            'position': 'SUPPORT',
            'comments': 'I support this bill.',
        }
        response = self.client.post('/api/legislation/feedback/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_submit_feedback_as_authenticated_user(self):
        user = User.objects.create_user(
            username='voter', password='StrongPass123!', ward=self.ward,
        )
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {
            'instrument': self.instrument.id,
            'full_name': 'Voter',
            'position': 'OPPOSE',
            'comments': 'I oppose this bill.',
        }
        response = self.client.post('/api/legislation/feedback/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        feedback = PublicFeedback.objects.get(full_name='Voter')
        self.assertEqual(feedback.user, user)
        self.assertEqual(feedback.ward_ref, self.ward)
        self.assertEqual(feedback.constituency_ref, self.constituency)

    def test_submit_amendment_feedback(self):
        data = {
            'instrument': self.instrument.id,
            'full_name': 'Amender',
            'position': 'AMEND',
            'comments': 'Please amend clause 5.',
            'target_clause': 'Section 5(2)',
            'proposed_alternative': 'Replace with new wording.',
        }
        response = self.client.post('/api/legislation/feedback/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_guest_cannot_delete_feedback(self):
        fb = PublicFeedback.objects.create(
            instrument=self.instrument, full_name='Test', position='SUPPORT', comments='Test',
        )
        response = self.client.delete(f'/api/legislation/feedback/{fb.id}/')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
