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

    def setUpAuthorization(self):
        self.jwt_token = generate_jwt_token(self.user.id)
        self.client.force_authenticate(user=self.user, token=self.jwt_token)

    def test_unauthorized_access(self):
        """Attempting to access without authentication"""

        response = self.client.post(
            path='/api/categories/',
            data=json.dumps({
                "title": "Mobile",
                "slug": "Mobile",
                "parent_pk": self.category1.id,
            }),
            content_type='application/json'
        )
        assert response.status_code == 401  # Expecting Unauthorized status code

    def test_retrieve_category(self):
        """Retrieve category details"""

        self.setUpAuthorization()

        response = self.client.get('/api/categories/{}/'.format(self.category1.slug))
        assert response.status_code == 200
        assert response.data['title'] == 'category1'

    def test_update_category(self):
        """Updating category details"""

        self.setUpAuthorization()

        data = {
            "title": "New Category Title",
            "slug": "new-category",
            "parent_pk": self.category1.id,
        }

        response = self.client.put(
            path=f'/api/categories/{self.category1.slug}/',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.data['title'] == 'New Category Title'

    def test_delete_category_with_children(self):
        """Attempt to delete a category with children"""

        self.setUpAuthorization()

        child_category = Category.objects.create(
            title='Child Category',
            slug='child-category',
            parent=self.category1,
        )
        child_category.save()

        response = self.client.delete(f'/api/categories/{self.category1.slug}/')
        assert response.status_code == 400  # Expecting Bad Request due to existing children

    def test_delete_category(self):
        """Deleting a category"""

        self.setUpAuthorization()

        response = self.client.delete(f'/api/categories/{self.category1.slug}/')
        assert response.status_code == 204  # Expecting No Content after successful deletion
