
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch
from user_account.models import CustomUser


class UserRegistrationTests(APITestCase):

    def setUp(self):
        self.url = reverse('register')  
        self.valid_payload = {
            "first_name": "Darshan",
            "last_name": "MT",
            "user_role": "docter",
            "email": "darshan@example.com",
            "phone_number": "1234567890",
            "address_line_1": "Street 123",
            "address_line_2": "Area XYZ",
            "city": "Bengaluru",
            "state": "Karnataka",
            "country": "India",
            "password": "StrongPass@123",
            "confirm_password": "StrongPass@123"
        }
        self.invalid_payload = {
            "first_name": "",
            "last_name": "",
            "email": "invalidemail",
            "password": "123",
            "confirm_password": "321"
        }

    def test_register_user_success(self):
        """Ensure we can register a new user with valid payload"""
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        user = CustomUser.objects.get(email="darshan@example.com")
        self.assertFalse(user.is_active)  

    def test_register_user_invalid_payload(self):
        """Ensure registration fails with invalid payload"""
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_register_user_duplicate_email(self):
        """Ensure duplicate email registration is not allowed"""
        self.client.post(self.url, self.valid_payload, format='json')
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserSigninTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='TestPassword123!',
            first_name='Test',
            last_name='User',
            phone_number='9998887776',
            user_role='docter',  
            is_active=True
        )
        self.url = reverse('signin')  

    def test_signin_success(self):
        """User can login with correct credentials"""
        payload = {
            'email': 'testuser@example.com',
            'password': 'TestPassword123!'
        }
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_signin_fail_wrong_password(self):
        """Login fails if password is wrong"""
        payload = {
            'email': 'testuser@example.com',
            'password': 'WrongPassword'
        }
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_signin_fail_inactive_user(self):
        """Inactive users cannot login"""
        inactive_user = CustomUser.objects.create_user(
            email='inactive@example.com',
            password='TestPassword123!',
            first_name='Inactive',
            last_name='User',
            phone_number='8887776665',
            user_role='nurse',
            is_active=False
        )
        payload = {
            'email': 'inactive@example.com',
            'password': 'TestPassword123!'
        }
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ResetPasswordTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('reset-password') 
        self.user = CustomUser.objects.create_user(
            email='resetuser@example.com',
            password='TestPassword123',
            first_name='Reset',
            last_name='User',
            user_role='docter',
            is_active=True
        )

    @patch('user_account.views.send_link') 
    def test_reset_password_valid_email(self, mock_send):
        """Ensure the reset link is sent for a valid email"""
        response = self.client.post(self.url, {'email': self.user.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertTrue(mock_send.called)

    def test_reset_password_invalid_email(self):
        """Ensure proper response if email does not exist"""
        response = self.client.post(self.url, {'email': 'nonexist@example.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'User with this email does not exist!')

    def test_reset_password_missing_email(self):
        """Ensure proper response if email is missing in request"""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Please provide your email!')
