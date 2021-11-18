from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """ Tests the users API (public = no authntication needed) """

    def setUp(self):
        self.client = APIClient()

    def test_user_created_success(self):
        """Test creating user with calid payload success"""
        payload = {
            'email': 'test.test@django.com',
            'password': 'testpass123!@#$%',
            'name' : 'Test'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_already_exists(self):
        payload = {
            'email': 'test.test@django.com',
            'password': 'testpass123!@#$%',
            'name' : 'Test'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short(self):
        '''Password must be more then 5 characters'''
        payload = {
            'email': 'test.test@django.com',
            'password': 'qwer',
            'name' : 'Test'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
        email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ Test that a token is created for the user"""

        payload = {
            'email': 'test.test@django.com',
            'password': 'testpass123',
            'name' : 'Test'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ Test that token is not created if credintials are invalid"""

        create_user(email='test@django.com', password="test123")
        payload = {
        'email': 'test.test@django.com',
        'password': 'wrong',
        'name' : 'Test'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """ Test that user is not created if no token"""

        payload = {
        'email': 'test.test@django.com',
        'password': 'testpass',
        'name' : 'Test'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ Test that token is not created is user doesn't exist"""
        res = self.client.post(TOKEN_URL, {'email': 'one', "password": ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
