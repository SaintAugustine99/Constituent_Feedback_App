from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from locations.models import County, Constituency, Ward
from accounts.models import User
from .models import Project, ProjectUpdate


class ProjectAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        county = County.objects.create(name='Nairobi', code='047')
        constituency = Constituency.objects.create(name='Westlands', county=county)
        self.ward = Ward.objects.create(name='Parklands', constituency=constituency)
        self.project = Project.objects.create(
            name='Road Construction',
            description='Building a new road in Parklands',
            ward=self.ward,
            budget_allocated=5000000,
            status='ONGOING',
            completion_percentage=40,
        )
        self.user = User.objects.create_user(username='auditor', password='StrongPass123!')
        self.token = Token.objects.create(user=self.user)

    def test_list_projects_public(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Road Construction')

    def test_retrieve_project_detail(self):
        response = self.client.get(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completion_percentage'], 40)

    def test_list_updates_by_project_id(self):
        ProjectUpdate.objects.create(
            project=self.project, user=self.user, comment='Progress is good',
        )
        response = self.client.get(f'/api/projects/updates/?project_id={self.project.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_updates_without_project_id_returns_empty(self):
        response = self.client.get('/api/projects/updates/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_update_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        data = {
            'project': self.project.id,
            'comment': 'Phase 2 has started',
        }
        response = self.client.post('/api/projects/updates/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        update = ProjectUpdate.objects.first()
        self.assertEqual(update.user, self.user)
        self.assertFalse(update.verified)

    def test_create_update_unauthenticated(self):
        data = {
            'project': self.project.id,
            'comment': 'Anonymous update',
        }
        response = self.client.post('/api/projects/updates/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_project_str(self):
        self.assertEqual(str(self.project), 'Road Construction - Parklands')
