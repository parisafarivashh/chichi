import pytest
from rest_framework.test import APITransactionTestCase

from api.models import Category
from authorize.helpers import generate_jwt_token
from authorize.models import User


class TestDeleteCategory(APITransactionTestCase):

    @classmethod
    @pytest.mark.django_db
    def setUp(cls):
        cls.admin_user = User.objects.create_superuser(
            title='admin',
            email='admin@example.com',
            password='password',
        )
        cls.admin_user.save()

        cls.user = User.objects.create_user(
            title='user1',
            email='user1@gmail.com',
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

    def test_delete_category(self):
        self.jwt_token = generate_jwt_token(self.admin_user.id)
        self.client.force_authenticate(
            user=self.admin_user,
            token=self.jwt_token
        )

        response = self.client.delete(
            path=f'/api/categories/{self.category2.slug}/',
        )
        assert response.status_code == 204

        with pytest.raises(Category.DoesNotExist):
            Category.objects.get(slug=self.category2.slug)

        response = self.client.delete(
            path=f'/api/categories/{self.category1.slug}/',
        )
        assert response.status_code == 400

