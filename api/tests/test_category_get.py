import pytest
from rest_framework.test import APITestCase

from ..helper import generate_jwt_token
from ..models import Category
from authorize.models import User


class TestCategory(APITestCase):

    @classmethod
    @pytest.mark.django_db
    def setUp(cls):
        cls.user = User.objects.create_superuser(
            title='parisa',
            email='parisafarivash@gmail.com',
            password='Mypassword',
        )
        cls.category1 = Category.objects.create(title='category1', slug='1')
        cls.subcategory1 = Category.objects.create(
            title='subcategory1', slug='2', parent=cls.category1
        )
        cls.subcategory2 = Category.objects.create(
            title='subcategory2', slug='3', parent=cls.category1
        )

    def test_get(self):
        """ This test for creating category

        Returns:
            Category
        """
        self.jwt_token = generate_jwt_token(self.user.id)
        self.client.force_authenticate(user=self.user, token=self.jwt_token)

        response = self.client.get(
            path=f'/api/categories/{self.category1.slug}/',
        )
        assert response.status_code == 200
        for category in response.json():
            assert category['parent'] is not None

