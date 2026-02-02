from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import County, Constituency, Ward, Official


class LocationHierarchyModelTests(TestCase):

    def setUp(self):
        self.county = County.objects.create(name='Nairobi', code='047')
        self.constituency = Constituency.objects.create(name='Westlands', county=self.county)
        self.ward = Ward.objects.create(name='Parklands', constituency=self.constituency)

    def test_county_str(self):
        self.assertEqual(str(self.county), '047 - Nairobi')

    def test_constituency_str(self):
        self.assertEqual(str(self.constituency), 'Westlands (Nairobi)')

    def test_ward_str(self):
        self.assertEqual(str(self.ward), 'Parklands - Westlands')

    def test_hierarchy_relationships(self):
        self.assertEqual(self.ward.constituency, self.constituency)
        self.assertEqual(self.constituency.county, self.county)
        self.assertIn(self.constituency, self.county.constituencies.all())
        self.assertIn(self.ward, self.constituency.wards.all())


class OfficialModelTests(TestCase):

    def setUp(self):
        self.county = County.objects.create(name='Nairobi', code='047')
        self.constituency = Constituency.objects.create(name='Westlands', county=self.county)
        self.ward = Ward.objects.create(name='Parklands', constituency=self.constituency)
        self.official = Official.objects.create(
            name='John Doe', title='MCA', ward=self.ward,
            constituency=self.constituency, county=self.county,
        )

    def test_official_str(self):
        self.assertEqual(str(self.official), 'John Doe (Member of County Assembly)')

    def test_official_title_display(self):
        self.assertEqual(self.official.get_title_display(), 'Member of County Assembly')


class CountyAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        County.objects.create(name='Nairobi', code='047')
        County.objects.create(name='Mombasa', code='001')

    def test_list_counties(self):
        response = self.client.get('/api/counties/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_counties_public_access(self):
        response = self.client.get('/api/counties/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ConstituencyAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.county = County.objects.create(name='Nairobi', code='047')
        self.other_county = County.objects.create(name='Mombasa', code='001')
        Constituency.objects.create(name='Westlands', county=self.county)
        Constituency.objects.create(name='Langata', county=self.county)
        Constituency.objects.create(name='Mvita', county=self.other_county)

    def test_filter_by_county_id(self):
        response = self.client.get(f'/api/constituencies/?county_id={self.county.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_no_county_id_returns_empty(self):
        response = self.client.get('/api/constituencies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class WardAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        county = County.objects.create(name='Nairobi', code='047')
        self.constituency = Constituency.objects.create(name='Westlands', county=county)
        other = Constituency.objects.create(name='Langata', county=county)
        Ward.objects.create(name='Parklands', constituency=self.constituency)
        Ward.objects.create(name='Highridge', constituency=self.constituency)
        Ward.objects.create(name='Karen', constituency=other)

    def test_filter_by_constituency_id(self):
        response = self.client.get(f'/api/wards/?constituency_id={self.constituency.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_no_constituency_id_returns_empty(self):
        response = self.client.get('/api/wards/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class OfficialAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        county = County.objects.create(name='Nairobi', code='047')
        self.constituency = Constituency.objects.create(name='Westlands', county=county)
        self.ward = Ward.objects.create(name='Parklands', constituency=self.constituency)
        Official.objects.create(name='MCA Person', title='MCA', ward=self.ward, county=county)
        Official.objects.create(name='MP Person', title='MP', constituency=self.constituency, county=county)

    def test_filter_by_ward_id(self):
        response = self.client.get(f'/api/locations/officials/?ward_id={self.ward.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'MCA Person')

    def test_no_filter_returns_all(self):
        response = self.client.get('/api/locations/officials/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
