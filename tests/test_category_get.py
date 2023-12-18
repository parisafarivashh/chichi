import json

import pytest
from rest_framework.test import APITransactionTestCase

from api.models import Category
from authorize.helpers import generate_jwt_token
from authorize.models import User


class TestGetCategory(APITransactionTestCase):

    @classmethod
    @pytest.mark.django_db
    def setUp(cls):
        cls.user = User.objects.create_user(
            title='parisa',
            email='parisafarivash@gmail.com',
            password='Mypassword',
        )

        cls.category1 = Category.objects.create(
            title='category1',
            slug='category1',
            parent=None,
        )

        cls.mobile_category = Category.objects.create(
            title='Mobile',
            slug='mobile',
            parent=cls.category1,
        )

    def test_get_category(self):
        self.jwt_token = generate_jwt_token(self.user.id)
        self.client.force_authenticate(user=self.user, token=self.jwt_token)

        response = self.client.get(
            path=f'/api/categories/{self.category1.slug}/',
        )
        assert response.status_code == 200

        assert response.data['id'] == self.category1.id
        assert response.data['title'] == self.category1.title
        assert response.data['slug'] == self.category1.slug
        assert response.data['parent'] is None

