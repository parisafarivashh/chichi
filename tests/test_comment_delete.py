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
        cls.admin = User.objects.create_superuser(
            title='admin',
            email='admin@example.com',
            password='Mypassword',
        )
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
        cls.comment3 = Comment.objects.create(
            body='comment3',
            is_approved=True,
            created_by=cls.user2,
            product=cls.product1,
        )

    def test_delete(self):
        """Delete Comment"""

        self.jwt_token = generate_jwt_token(self.user1.id)
        self.client.force_authenticate(user=self.user1, token=self.jwt_token)

        response = self.client.delete(
            path=f'/api/products/{self.product1.id}/comments/{self.comment1.id}',
            content_type='application/json'
        )
        assert response.status_code == 204

        # when user is not admin, user can not delete others comment
        response = self.client.delete(
            path=f'/api/products/{self.product1.id}/comments/{self.comment3.id}',
            content_type='application/json'
        )
        assert response.status_code == 403

        self.jwt_token = generate_jwt_token(self.admin.id)
        self.client.force_authenticate(user=self.admin, token=self.jwt_token)
        # when user is admin, admin can delete others comment
        response = self.client.delete(
            path=f'/api/products/{self.product1.id}/comments/{self.comment3.id}',
            content_type='application/json'
        )
        assert response.status_code == 204

        response = self.client.delete(
            path=f'/api/products/{self.product1.id}/comments/{0}',
            content_type='application/json'
        )
        assert response.status_code == 404

        response = self.client.delete(
            path=f'/api/products/{self.product1.id}/comments/{"0"}',
            content_type='application/json'
        )
        assert response.status_code == 404

