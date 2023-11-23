from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from ..serializers.category import CategorySerializer
from ..views.category import CategoryView

from ..models import User, Category


class CategoryViewTest(APITestCase):
    def setUp(self):
        # Create a user with admin privileges
        self.admin_user = User.objects.create_superuser(
            title='admin',
            email='admin@gmail.com',
            password='admin123',
        )
        self.admin_user.save()

        # Create some categories
        Category.objects.create(title='Category 1', slug='c1')
        Category.objects.create(title='Category 2', slug='c2', parent=None)
        Category.objects.create(
            title='Subcategory 1',
            slug='c3',
            parent=Category.objects.get(title='Category 1')
        )

    def test_list_categories(self):
        url = reverse('Create_list_category')
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the serialized data matches the expected data
        expected_data = CategorySerializer(
            Category.objects.filter(parent__isnull=True),
            many=True
        ).data
        self.assertEqual(response.data, expected_data)

    def test_unauthenticated_access(self):
        url = reverse('Create_list_category')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_queryset(self):
        view = CategoryView()
        queryset = view.get_queryset()

        # Ensure that the queryset contains only top-level categories
        self.assertTrue(all(category.parent is None for category in queryset))

