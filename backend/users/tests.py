from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
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

class LoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('login')
        self.user = User.objects.create_user(
            username='john',
            email='john@test.com',
            password='secret123'
        )

    def test_login_returns_tokens(self):
        response = self.client.post(self.url, {
            'username': 'john',
            'password': 'secret123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_wrong_password_returns_401(self):
        response = self.client.post(self.url, {
            'username': 'john',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class MeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('me')
        self.user = User.objects.create_user(
            username='john',
            email='john@test.com',
            password='secret123'
        )

    def get_auth_client(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        return self.client

    def test_me_returns_user_data(self):
        client = self.get_auth_client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'john')
        self.assertEqual(response.data['email'], 'john@test.com')

    def test_me_requires_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_password_not_exposed(self):
        client = self.get_auth_client()
        response = client.get(self.url)
        self.assertNotIn('password', response.data)
