from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import Category


class CategorySerializer(ModelSerializer):
    parent_pk = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='parent',
        write_only=True,
        required=False
    )

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'parent', 'children', 'parent_pk']
        depth = 10
        extra_kwargs = dict(
            parent_pk=dict(required=False),
            children=dict(required=False),
            parent=dict(required=False),
        )

