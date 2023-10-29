import json

import pytest
from rest_framework.test import APITestCase

from ..helper import generate_jwt_token
from ..models import User


class TestCategory(APITestCase):

    @classmethod
    @pytest.mark.django_db
    def setUp(cls):
        cls.user = User.objects.create_user(
            title='parisa',
            email='parisafarivash@gmail.com',
            password='Mypassword',
        )

    def test_create_category(self):
        """ This test for creating category

        Returns:
            Category
        """
        self.jwt_token = generate_jwt_token(self.user.id)
        self.client.force_authenticate(user=self.user, token=self.jwt_token)

        data = json.dumps({
            "title": "Mobile",
            "slug": "Mobile",
            "parent": ""
        })

        response = self.client.post(
            path='/api/categories/',
            data=data,
            content_type='application/json'
        )
        assert response.status_code == 201
        assert response.data['id'] is not None
        assert response.data['title'] == 'Mobile'
