# accounts/tests.py

import re
from django.urls import reverse
from django.test import TestCase, override_settings
from django.core import mail
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('account-register')
        self.activate_url = lambda uid, token: reverse('account-activate', args=[uid, token])
        self.login_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
        self.password_reset_url = reverse('password_reset')
        self.password_reset_confirm_url = lambda uid, token: reverse('password_reset_confirm', args=[uid, token])
        self.logout_url = reverse('account-logout')

    def test_registration_and_activation(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPass123!",
            "account_type": "contractor",
            "full_name": "Test User",
            "company_name": ""
        }
        # Registration
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, 201)
        # Email sent
        self.assertEqual(len(mail.outbox), 1)
        email_body = mail.outbox[0].body
        # Extract uid and token
        match = re.search(r'/api/accounts/activate/(\d+)/([\w\-]+)/', email_body)
        self.assertIsNotNone(match)
        uid, token = match.groups()
        # Activation
        response = self.client.get(self.activate_url(uid, token))
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(pk=uid)
        self.assertTrue(user.is_active)

    def test_login_and_refresh(self):
        # Create and activate user
        user = User.objects.create_user(
            username='testlogin',
            email='login@example.com',
            password='LoginPass123!',
            account_type='contractor',
            full_name='Login User'
        )
        user.is_active = True
        user.save()
        # Obtain JWT
        response = self.client.post(self.login_url,
                                    {'username': 'testlogin', 'password': 'LoginPass123!'},
                                    format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        # Refresh token
        refresh = response.data['refresh']
        response = self.client.post(self.refresh_url, {'refresh': refresh}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_password_reset_flow(self):
        # Create and activate user
        user = User.objects.create_user(
            username='resetuser',
            email='reset@example.com',
            password='OldPass123!',
            account_type='contractor',
            full_name='Reset User'
        )
        user.is_active = True
        user.save()
        # Request reset
        response = self.client.post(self.password_reset_url,
                                    {'email': 'reset@example.com'},
                                    format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        email_body = mail.outbox[0].body
        # Extract uid and token
        match = re.search(r'/api/accounts/password-reset-confirm/(\d+)/([\w\-]+)/', email_body)
        self.assertIsNotNone(match)
        uid, token = match.groups()
        # Confirm reset
        new_password = 'NewPass123!'
        response = self.client.post(
            self.password_reset_confirm_url(uid, token),
            {'password': new_password},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        # Login with new password
        response = self.client.post(self.login_url,
                                    {'username': 'resetuser', 'password': new_password},
                                    format='json')
        self.assertEqual(response.status_code, 200)

    def test_logout_blacklist(self):
        # Create & activate user
        user = User.objects.create_user(
            username='logoutuser',
            email='logout@example.com',
            password='LogoutPass123!',
            account_type='contractor',
            full_name='Logout User'
        )
        user.is_active = True
        user.save()

        # 1Login to get tokens
        login_resp = self.client.post(self.login_url,
                                      {'username': 'logoutuser', 'password': 'LogoutPass123!'},
                                      format='json')
        self.assertEqual(login_resp.status_code, 200)
        access = login_resp.data['access']
        refresh = login_resp.data['refresh']

        # 2Authenticate the client with the access token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

        # 3Call logout with the refresh token
        response = self.client.post(self.logout_url,
                                    {'refresh': refresh},
                                    format='json')
        self.assertEqual(response.status_code, 204)

        # 4Subsequent refresh must fail
        resp2 = self.client.post(self.refresh_url, {'refresh': refresh}, format='json')
        self.assertEqual(resp2.status_code, 401)
