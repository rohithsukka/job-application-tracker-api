"""Automated tests for the job application tracker API."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import JobApplication


class JobApplicationAPITests(APITestCase):
    """Covers the minimum API scenarios requested in the assignment."""

    def test_create_application(self):
        """A valid POST request should create a new job application."""
        url = reverse('application-list')
        data = {
            'company': 'Google',
            'role': 'Backend Engineer',
            'status': 'applied',
            'notes': 'Applied through careers portal',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobApplication.objects.count(), 1)
        self.assertEqual(JobApplication.objects.first().company, 'Google')

    def test_filter_applications_by_status(self):
        """The list endpoint should support filtering with ?status=..."""
        JobApplication.objects.create(
            company='Google',
            role='Backend Engineer',
            status='applied',
            notes='First application',
        )
        JobApplication.objects.create(
            company='Amazon',
            role='Software Engineer',
            status='rejected',
            notes='Second application',
        )

        url = reverse('application-list')
        response = self.client.get(url, {'status': 'applied'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'applied')

    def test_summary_endpoint_structure(self):
        """The summary response should always expose all required status keys."""
        JobApplication.objects.create(
            company='Google',
            role='Backend Engineer',
            status='applied',
        )
        JobApplication.objects.create(
            company='Amazon',
            role='Software Engineer',
            status='rejected',
        )

        url = reverse('application-summary')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('applied', response.data)
        self.assertIn('interviewing', response.data)
        self.assertIn('rejected', response.data)
        self.assertIn('offered', response.data)
        self.assertIsInstance(response.data['applied'], int)
        self.assertIsInstance(response.data['interviewing'], int)
        self.assertIsInstance(response.data['rejected'], int)
        self.assertIsInstance(response.data['offered'], int)
