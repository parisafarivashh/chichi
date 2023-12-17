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
        cls.admin = User.objects.create_superuser(
            title='admin',
            email='admin@example.com',
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

    def test_list(self):
        """List Comment"""

        self.jwt_token = generate_jwt_token(self.user1.id)
        self.client.force_authenticate(user=self.user1, token=self.jwt_token)

        # When user is not admin, get list approved comments
        response = self.client.get(
            path=f'/api/products/{self.product1.id}/comments',
            content_type='application/json'
        )
        assert response.status_code == 200
        assert len(response.data['results']) == 2
        assert response.data['count'] == 2
        assert response.data['next'] is None
        assert response.data['previous'] is None
        for comment in response.data['results']:
            assert comment['id'] in [self.comment2.id, self.comment3.id]
            assert comment['is_approved'] is True

        self.jwt_token = generate_jwt_token(self.admin.id)
        self.client.force_authenticate(user=self.admin, token=self.jwt_token)

        # When user is admin, get list all comments
        response = self.client.get(
            path=f'/api/products/{self.product1.id}/comments',
            content_type='application/json'
        )
        assert response.status_code == 200
        assert len(response.data['results']) == 3
        for comment in response.data['results']:
            assert comment['id'] in [
                self.comment1.id,
                self.comment2.id,
                self.comment3.id,
            ]
            assert comment['is_approved'] in [True, False]

        # When user is admin, filtering with is_approved False
        response = self.client.get(
            path=f'/api/products/{self.product1.id}/comments',
            data={'is_approved': 'False'},
            content_type='application/json',
        )
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        for comment in response.data['results']:
            assert comment['id'] == self.comment1.id
            assert comment['is_approved'] is False

        # When user is admin, filtering with is_approved True and limit 1
        response = self.client.get(
            path=f'/api/products/{self.product1.id}/comments',
            data={'is_approved': 'True', 'limit': '1'},
            content_type='application/json',
        )
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        for comment in response.data['results']:
            assert comment['id'] == self.comment2.id
            assert comment['is_approved'] is True

