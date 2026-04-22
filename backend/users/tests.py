from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User

class RegisterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')
        self.valid_payload = {
            'username': 'Joanne',
            'email': 'test@email.com',
            'password': 'password123'
        }
    def test_register_success(self):
        response = self.client.post(self.url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'Joanne')
    
    def test_password_is_hashed(self):
        self.client.post(self.url, self.valid_payload)
        user = User.objects.get(username='Joanne')
        self.assertNotEqual(user.password, 'password123')
    
    def test_password_not_in_response(self):
        response = self.client.post(self.url, self.valid_payload)
        self.assertNotIn('password', response.data)

    def test_duplicate_email_returns_400(self):
        self.client.post(self.url, self.valid_payload)
        response = self.client.post(self.url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_fields_returns_400(self):
        response = self.client.post(self.url, {'username': 'john'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_password_returns_400(self):
        payload = {**self.valid_payload, 'password': '123'}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
