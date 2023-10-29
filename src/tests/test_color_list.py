import pytest
from rest_framework.test import APITestCase

from ..helper import generate_jwt_token
from ..models import Color, User


class TestColor(APITestCase):

    @classmethod
    @pytest.mark.django_db()
    def setUpTestData(cls):  # or setUp
        cls.color1 = Color.objects.create(title='c1', slug='1')
        cls.color2 = Color.objects.create(title='c2', slug='2')
        cls.color3 = Color.objects.create(title='c3', slug='3')
        cls.color4 = Color.objects.create(title='c4', slug='4')
        cls.user = User.objects.create_user(
            title='parisa',
            email='parisafarivash@gmail.com',
            password='Mypassword',
        )

    def test_list_color(self):
        """ This test get all colors

        Returns:
            Colors
        """
        self.jwt_token = generate_jwt_token(self.user.id)
        self.client.force_authenticate(user=self.user, token=self.jwt_token)

        response = self.client.get(
            path='/api/colors/',
            content_type='application/json'
        )
        assert response.status_code == 200
        for color in response.json():
            assert color['id'] is not None
            assert color['title'] is not None
