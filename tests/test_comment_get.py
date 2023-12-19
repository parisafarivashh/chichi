import json

import pytest
from rest_framework.test import APITransactionTestCase

from api.models import Product, Comment
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
        cls.user2 = User.objects.create_user(
            title='user2',
            email='user2@example.com',
            password='Mypassword',
        )

        cls.product1 = Product.objects.create(
            title='product 1',
            description='description 1',
            created_by=cls.user1,
        )
        cls.comment1 = Comment.objects.create(
            body='comment1',
            is_approved=False,
            created_by=cls.user1,
            product=cls.product1,
        )
        cls.comment2 = Comment.objects.create(
            body='comment2',
            is_approved=True,
            created_by=cls.user1,
            product=cls.product1,
        )

    def test_get(self):
        """getting Comment"""

        response = self.client.get(
            path=f'/api/products/{self.product1.id}/comments/{self.comment1.id}',
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.data['id'] is not None
        assert response.data['body'] == self.comment1.body
        assert response.data['created_by'] == self.user1.id

        response = self.client.get(
            path=f'/api/products/{self.product1.id}/comments/{self.comment2.id}',
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.data['id'] is not None
        assert response.data['body'] == self.comment2.body
        assert response.data['created_by'] == self.user1.id

        self.jwt_token = generate_jwt_token(self.user2.id)
        self.client.force_authenticate(user=self.user2, token=self.jwt_token)

        response = self.client.get(
            path=f'/api/products/{self.product1.id}/comments/{self.comment2.id}',
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.data['id'] is not None
        assert response.data['body'] == self.comment2.body
        assert response.data['created_by'] == self.user1.id

        response = self.client.get(
            path=f'/api/products/{self.product1.id}/comments/{0}',
            content_type='application/json'
        )
        assert response.status_code == 404

        response = self.client.get(
            path=f'/api/products/{self.product1.id}/comments/{"0"}',
            content_type='application/json'
        )
        assert response.status_code == 404

