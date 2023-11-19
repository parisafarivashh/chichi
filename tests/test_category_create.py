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
        assert len(response.data) == 1
        assert response.data[0]['title'] == self.category1.title
        assert response.data[0]['parent'] is None
        assert response.data[0]['children'] is not None
        assert response.data[0]['children'][0]['title'] == 'Mobile'
        assert response.data[0]['children'][0]['parent']['id'] == response.data[0]['id']

