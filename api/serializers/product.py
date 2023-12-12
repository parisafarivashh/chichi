from rest_framework.serializers import ModelSerializer

from ..models import Product


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'status', 'created_by', 'rate']
        extra_kwargs = {
            'created_by': {'required': False},
            'rate': {'required': False, 'read_only': True},
        }

