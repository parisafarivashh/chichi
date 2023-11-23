import jwt
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import User


class TestMyTokenObtainPairView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            title='testuser',
            email='test@example.com',
            password='testpassword',
        )

    def test_get_token(self):
        url = reverse('token_obtain_pair')

        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data.get('access', None)
        self.assertIsNotNone(token)

        # assert serializer.is_valid() is True
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        self.assertEqual(decoded_token['id'], self.user.id)
        self.assertEqual(decoded_token['title'], self.user.title)
        self.assertEqual(decoded_token['email'], self.user.email)

    def test_invalid_credentials(self):
        url = reverse('token_obtain_pair')

        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'  # Invalid password
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

