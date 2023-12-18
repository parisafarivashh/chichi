import pytest
from rest_framework.test import APITransactionTestCase

from api.models import Category
from authorize.helpers import generate_jwt_token
from authorize.models import User


class TestCategory(APITransactionTestCase):

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

        cls.category1 = Category.objects.create(
            title='Mobile',
            slug='mobile',
            parent=None,
        )
        cls.category1.save()

        cls.category2 = Category.objects.create(
            title='LG',
            slug='lg',
            parent=cls.category1,
        )
        cls.category2.save()

    def test_update(self):
        self.jwt_token = generate_jwt_token(self.admin_user.id)
        self.client.force_authenticate(
            user=self.admin_user,
            token=self.jwt_token,
        )

        response = self.client.put(
            path=f'/api/categories/{self.category2.slug}/',
            data={
                "title": "Nokia",
                "slug": "nokia",
            },
            format='json',
        )
        assert response.status_code == 200
        assert response.data['id'] is not None
        assert response.data['title'] == 'Nokia'

        updated_category = Category.objects.get(id=response.data['id'])
        assert updated_category.title == "Nokia"
        assert updated_category.parent == self.category1

