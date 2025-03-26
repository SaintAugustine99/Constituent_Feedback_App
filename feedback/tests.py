from django.test import TestCase

# Create your tests here.
# feedback/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User, District
from feedback.models import Category, Feedback

class FeedbackAPITestCase(TestCase):
    def setUp(self):
        # Create a test district
        self.district = District.objects.create(name="Test District")
        
        # Create a test user
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
            district=self.district
        )
        
        # Create a test admin
        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="adminpassword",
            first_name="Admin",
            last_name="User",
            role=User.ADMIN
        )
        
        # Create a test category
        self.category = Category.objects.create(name="Test Category")
        
        # Create a test feedback
        self.feedback = Feedback.objects.create(
            user=self.user,
            title="Test Feedback",
            description="This is a test feedback",
            category=self.category
        )
        
        # Setup API client
        self.client = APIClient()
    
    def test_list_feedback_authenticated(self):
        # Authenticate as normal user
        self.client.force_authenticate(user=self.user)
        
        # Make request
        url = reverse('feedback-list-create')
        response = self.client.get(url)
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should only see their own feedback
    
    def test_list_feedback_admin(self):
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin)
        
        # Make request
        url = reverse('feedback-list-create')
        response = self.client.get(url)
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should see all feedback
    
    def test_create_feedback(self):
        # Authenticate as normal user
        self.client.force_authenticate(user=self.user)
        
        # Prepare data
        data = {
            "title": "New Feedback",
            "description": "This is a new feedback",
            "category": self.category.id
        }
        
        # Make request
        url = reverse('feedback-list-create')
        response = self.client.post(url, data, format='json')
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Feedback")
        
        # Check database
        self.assertEqual(Feedback.objects.count(), 2)