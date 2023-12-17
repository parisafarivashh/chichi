import json

import pytest
from rest_framework.test import APITransactionTestCase

from api.models import Product
from authorize.helpers import generate_jwt_token
from authorize.models import User


class TestComment(APITransactionTestCase):

    @classmethod
    @pytest.mark.django_db
    def setUp(cls):
        cls.user1 = User.objects.create_user(
            title='user1',
            email='user1@example.com',
            password='Mypassword',
        )

        cls.product1 = Product.objects.create(
            title='product 1',
            description='description 1',
            created_by=cls.user1,
        )

    def test_create(self):
        """Creating Comment"""

        self.jwt_token = generate_jwt_token(self.user1.id)
        self.client.force_authenticate(user=self.user1, token=self.jwt_token)

        response = self.client.post(
            path=f'/api/products/{self.product1.id}/comments',
            data=json.dumps({
                'body': 'test',
            }),
            content_type='application/json'
        )
        assert response.status_code == 201
        assert response.data['id'] is not None
        assert response.data['body'] == 'test'
        assert response.data['is_approved'] is False

        response = self.client.post(
            path=f'/api/products/{self.product1.id}/comments',
            data=json.dumps({
                'is_approved': True,
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
        assert response.json()['body'] == ['This field is required.']

        response = self.client.post(
            path=f'/api/products/{0}/comments',
            data=json.dumps({
                'body': 'hi',
            }),
            content_type='application/json'
        )
        assert response.status_code == 404

        response = self.client.post(
            path=f'/api/products/{"a"}/comments',
            data=json.dumps({
                'body': 'hi',
            }),
            content_type='application/json'
        )
        assert response.status_code == 404

