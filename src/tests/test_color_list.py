import pytest
from rest_framework.test import APITestCase

from ..models import Color


class TestColor(APITestCase):

    @classmethod
    @pytest.mark.django_db()
    def setUpTestData(cls):  # or setUp
        cls.color1 = Color.objects.create(title='c1')
        cls.color2 = Color.objects.create(title='c2')
        cls.color3 = Color.objects.create(title='c3')
        cls.color4 = Color.objects.create(title='c4')

    def test_list_color(self):
        """ This test get all colors

        Returns:
            Colors
        """
        response = self.client.get(
            path='/api/colors/',
            content_type='application/json'
        )
        assert response.status_code == 200
        for color in response.json():
            assert color['id'] is not None
            assert color['title'] is not None
