import pytest
from rest_framework.test import APITransactionTestCase

from api.models import Product
from authorize.helpers import generate_jwt_token
from authorize.models import User


class TestProduct(APITransactionTestCase):

    @classmethod
    @pytest.mark.django_db
    def setUp(cls):
        cls.user1 = User.objects.create_user(
            title='user1',
            email='user1@example.com',
            password='password',
        )

        cls.admin_user = User.objects.create_superuser(
            title='admin',
            email='admin@example.com',
            password='password',
        )

        cls.product1 = Product.objects.create(
            title='product1',
            description='product1',
            created_by=cls.admin_user,
        )
        cls.product1.save()

        cls.product2 = Product.objects.create(
            title='product2',
            description='product2',
            created_by=cls.admin_user,
            status=Product.ProductStatus.DEACTIVATED,
        )
        cls.product2.save()

    def test_get(self):
        self.jwt_token = generate_jwt_token(self.user1.id)
        self.client.force_authenticate(user=self.user1, token=self.jwt_token)

        response = self.client.get(
            path=f'/api/products/{self.product1.id}/',
        )
        assert response.status_code == 200

        response = self.client.get(
            path=f'/api/products/0/',
        )
        assert response.status_code == 404

        response = self.client.get(
            path=f'/api/products/{self.product2.id}/',
        )
        assert response.status_code == 404

