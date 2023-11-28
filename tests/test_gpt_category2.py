from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from api.models import Category
from authorize.models import User


class TestCategoryViews(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            title='parisa',
            email='parisafarivash@gmail.com',
            password='Mypassword',
        )
        cls.admin_user = User.objects.create_superuser(
            title='admin',
            email='admin@example.com',
            password='AdminPass123',
        )

        cls.category1 = Category.objects.create(
            title='category1',
            slug='category1',
            parent=None,
        )

    def setUp(self):
        self.jwt_token = AccessToken.for_user(self.user)
        self.admin_jwt_token = AccessToken.for_user(self.admin_user)

    def test_list_categories_unauthenticated(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_categories_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.jwt_token}')
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category_unauthenticated(self):
        data = {
            "title": "Mobile",
            "slug": "Mobile",
            "parent_pk": self.category1.id,
        }
        response = self.client.post('/api/categories/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_category_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.jwt_token}')
        data = {
            "title": "Mobile",
            "slug": "Mobile",
            "parent_pk": self.category1.id,
        }
        response = self.client.post('/api/categories/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Mobile')

    def test_create_category_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_jwt_token}')
        data = {
            "title": "Electronics",
            "slug": "electronics",
            "parent_pk": None,  # Assuming it's a top-level category
        }
        response = self.client.post('/api/categories/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Electronics')

    def test_retrieve_category(self):
        response = self.client.get(f'/api/categories/{self.category1.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'category1')

    def test_update_category_unauthenticated(self):
        data = {
            "title": "Updated Category",
            "slug": "updated-category",
            "parent_pk": self.category1.id,
        }
        response = self.client.put(f'/api/categories/{self.category1.slug}/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # More tests for update, delete, and other scenarios based on different permission classes can be added here
