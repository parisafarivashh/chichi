from rest_framework.serializers import ModelSerializer

from ..models import Color


class ColorSerializer(ModelSerializer):

    class Meta:
        model = Color
        fields = ['id', 'title', 'code', 'slug']

