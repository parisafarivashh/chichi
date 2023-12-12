import json

import pytest
from rest_framework.test import APITransactionTestCase

from api.models import Product
from authorize.helpers import generate_jwt_token
from authorize.models import User


class TestProduct(APITransactionTestCase):

    @classmethod
    @pytest.mark.django_db
    def setUp(cls):
        cls.admin_user = User.objects.create_superuser(
            title='admin',
            email='admin@example.com',
            password='password',
        )
        cls.admin_user.save()

        cls.user1 = User.objects.create_user(
            title='user1',
            email='user1@example.com',
            password='password',
        )

        cls.product1 = Product.objects.create(
            title='product1',
            description='product1',
            created_by=cls.admin_user,
        )
        cls.product1.save()

    def test_create(self):
        self.jwt_token = generate_jwt_token(self.admin_user.id)
        self.client.force_authenticate(user=self.admin_user, token=self.jwt_token)
        data = json.dumps(dict(
            title='New product',
            description='this is description of product',
        ))

        response = self.client.post(
            path='/api/products/',
            data=data,
            content_type='application/json'
        )
        assert response.status_code == 201
        assert response.data['id'] is not None
        assert response.data['title'] == 'New product'

