from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import Category


class CategorySerializer(ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='parent', write_only=True,
    )

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'parent', 'parent_id', 'children']
        depth = 10

