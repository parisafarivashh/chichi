import json

import pytest
from rest_framework.test import APITransactionTestCase

from api.models import Category
from authorize.helpers import generate_jwt_token
from authorize.models import User


class TestCategory(APITransactionTestCase):

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
        cls.category1.save()

    def test_create(self):
        """Creating category"""

        self.jwt_token = generate_jwt_token(self.user.id)
        self.client.force_authenticate(user=self.user, token=self.jwt_token)

        data = json.dumps({
            "title": "Mobile",
            "slug": "Mobile",
            "parent_pk": self.category1.id,
        })

        response = self.client.post(
            path='/api/categories/',
            data=data,
            content_type='application/json'
        )
        assert response.status_code == 201
        assert response.data['id'] is not None
        assert response.data['title'] == 'Mobile'

        response = self.client.get(
            path='/api/categories/',
        )
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        for category in response.data['results']:
            assert category['title'] == self.category1.title
            assert category['parent'] is None
            assert category['children'] is not None
            assert category['children'][0]['title'] == 'Mobile'
            assert category['children'][0]['parent']['id'] == category['id']

