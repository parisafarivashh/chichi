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

        cls.product2 = Product.objects.create(
            title='product2',
            description='product2',
            created_by=cls.admin_user,
            status=Product.ProductStatus.DEACTIVATED,
        )
        cls.product2.save()

    def test_update(self):
        self.jwt_token = generate_jwt_token(self.admin_user.id)
        self.client.force_authenticate(user=self.admin_user, token=self.jwt_token)

        updated_data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'created_by_pk': self.admin_user.id,
            'status': Product.ProductStatus.ACTIVE
        }

        response = self.client.put(
            path=f'/api/products/{self.product1.id}/',
            data=updated_data,
            format='json'
        )
        assert response.status_code == 200

        updated_product = Product.objects.get(id=self.product1.id)
        assert updated_product.title == updated_data['title']
        assert updated_product.description == updated_data['description']
        assert updated_product.status == updated_data['status']

        # TODO: this test must be pass
        response = self.client.put(
            path=f'/api/products/{self.product2.id}/',
            data=updated_data,
            format='json'
        )
        assert response.status_code == 404

        response = self.client.put(
            path='/api/products/0/',
            data=updated_data,
            format='json'
        )
        assert response.status_code == 404

