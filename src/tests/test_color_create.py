import json

from rest_framework.test import APITestCase


class TestColor(APITestCase):

    def test_create_color(self):
        """ This test for creating color

        Returns:
            Color
        """
        data = json.dumps({
            "title": "blue",
            "code": "FF00",
        })

        response = self.client.post(
            path='/api/colors/',
            data=data,
            content_type='application/json'
        )
        assert response.status_code == 201
        assert response.data['id'] is not None
        assert response.data['title'] == 'blue'
