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

    def test_update(self):
        """Updating Comment"""

        self.jwt_token = generate_jwt_token(self.user1.id)
        self.client.force_authenticate(user=self.user1, token=self.jwt_token)

        response = self.client.patch(
            path=f'/api/products/{self.product1.id}/comments/{self.comment1.id}',
            data=json.dumps({
                'body': 'test',
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.data['id'] is not None
        assert response.data['body'] == 'test'
        assert response.data['created_by'] == self.user1.id

        # when user is not admin, user can not update is_approved field
        response = self.client.patch(
            path=f'/api/products/{self.product1.id}/comments/{self.comment1.id}',
            data=json.dumps({
                'body': 'test 2',
                'is_approved': True,
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.data['id'] is not None
        assert response.data['body'] == 'test 2'
        assert response.data['created_by'] == self.user1.id
        assert response.data['is_approved'] is False

        self.jwt_token = generate_jwt_token(self.admin.id)
        self.client.force_authenticate(user=self.admin, token=self.jwt_token)

        # when user is admin, user can update is_approved field for comments
        response = self.client.patch(
            path=f'/api/products/{self.product1.id}/comments/{self.comment1.id}',
            data=json.dumps({'is_approved': True}),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.data['id'] is not None
        assert response.data['body'] == 'test 2'
        assert response.data['created_by'] == self.user1.id
        assert response.data['is_approved'] is True

        self.jwt_token = generate_jwt_token(self.user2.id)
        self.client.force_authenticate(user=self.user2, token=self.jwt_token)

        # user 2 do not have access to comment of user 1
        response = self.client.patch(
            path=f'/api/products/{self.product1.id}/comments/{self.comment2.id}',
            data=json.dumps({'body': 'test 3'}),
            content_type='application/json'
        )
        assert response.status_code == 403

        response = self.client.patch(
            path=f'/api/products/{self.product1.id}/comments/{0}',
            data=json.dumps({'body': 'test 4'}),
            content_type='application/json'
        )
        assert response.status_code == 404

        response = self.client.patch(
            path=f'/api/products/{self.product1.id}/comments/{"0"}',
            data=json.dumps({'body': 'test 5'}),
            content_type='application/json'
        )
        assert response.status_code == 404

