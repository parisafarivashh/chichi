from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import Category


class CategorySerializer(ModelSerializer):
    parent_pk = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='parent',
        write_only=True,
    )

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'parent', 'children', 'parent_pk']
        depth = 10

