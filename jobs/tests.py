from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Job

User = get_user_model()


class JobCreationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.job_url = reverse('job-list-create')

        self.company = User.objects.create_user(
            username='techcorp', password='pass123', role='company', company_name='TechCorp'
        )
        self.job_seeker = User.objects.create_user(
            username='janedoe', password='pass123', role='job_seeker'
        )

    def test_company_can_create_job(self):
        self.client.force_authenticate(user=self.company)
        data = {
            'title': 'Backend Developer',
            'description': 'We need a Django dev',
            'location': 'Nairobi',
            'job_type': 'full_time',
        }
        response = self.client.post(self.job_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 1)

    def test_job_seeker_cannot_create_job(self):
        self.client.force_authenticate(user=self.job_seeker)
        data = {
            'title': 'Backend Developer',
            'description': 'We need a Django dev',
            'location': 'Nairobi',
            'job_type': 'full_time',
        }
        response = self.client.post(self.job_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anyone_can_view_job_list(self):
        response = self.client.get(self.job_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)