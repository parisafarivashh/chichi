from rest_framework.serializers import ModelSerializer

from ..models import Category


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'slug', 'parent']


class CategoryGetSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'slug', 'parent']

