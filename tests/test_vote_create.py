import json

import pytest
from rest_framework.test import APITransactionTestCase

from api.models import Product, Vote
from authorize.helpers import generate_jwt_token
from authorize.models import User


class TestVote(APITransactionTestCase):

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

        cls.vote1 = Vote.objects.create(
            rate=1,
            product=cls.product1,
            created_by=cls.user1,
        )

    def test_create(self):
        """Creating vote"""

        self.jwt_token = generate_jwt_token(self.user1.id)
        self.client.force_authenticate(user=self.user1, token=self.jwt_token)

        response = self.client.post(
            path=f'/api/products/{self.product1.id}/votes',
            data=json.dumps({
                'rate': 4,
            }),
            content_type='application/json'
        )
        assert response.status_code == 201
        assert response.data['id'] is not None
        assert response.data['rate'] == 4

        self.product1 = Product.objects.get(id=self.product1.id)
        assert self.product1.rate == 2

        response = self.client.post(
            path=f'/api/products/{self.product1.id}/votes',
            data=json.dumps({
                'rate': 10,
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
        assert response.json()['rate'] == [
            'Ensure this value is less than or equal to 5.',
        ]

        response = self.client.post(
            path=f'/api/products/{self.product1.id}/votes',
            data=json.dumps({
                'rate': -2,
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
        assert response.json()['rate'] == [
            'Ensure this value is greater than or equal to 0.',
        ]

        response = self.client.post(
            path=f'/api/products/{0}/votes',
            data=json.dumps({
                'rate': 4,
            }),
            content_type='application/json'
        )
        assert response.status_code == 404

        response = self.client.post(
            path=f'/api/products/{"a"}/votes',
            data=json.dumps({
                'rate': 4,
            }),
            content_type='application/json'
        )
        assert response.status_code == 404
