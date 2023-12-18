import json

import pytest
from rest_framework.test import APITransactionTestCase

from api.models import Category
from authorize.helpers import generate_jwt_token
from authorize.models import User


class TestListCategory(APITransactionTestCase):

    @classmethod
    @pytest.mark.django_db
    def setUp(cls):
        cls.user = User.objects.create_user(
            title='admin',
            email='admin@gmail.com',
            password='password',
        )

        cls.category1 = Category.objects.create(
            title='category1',
            slug='category1',
            parent=None,
        )
        cls.category2 = Category.objects.create(
            title='category2',
            slug='category2',
            parent=None,
        )

        cls.mobile_category = Category.objects.create(
            title='Mobile',
            slug='mobile',
            parent=cls.category1,
        )

    def test_list_categories(self):
        self.jwt_token = generate_jwt_token(self.user.id)
        self.client.force_authenticate(user=self.user, token=self.jwt_token)

        response = self.client.get(path='/api/categories/')
        assert response.status_code == 200

        assert len(response.data['results']) == 2
        response = response.data['results']
        assert response[0]['title'] == self.category1.title
        assert response[1]['title'] == self.category2.title

        assert len(response[0]['children']) == 1
        assert response[0]['children'][0]['title'] == \
               self.mobile_category.title
        assert response[0]['children'][0]['parent']['id'] == response[0]['id']

        assert len(response[1]['children']) == 0

