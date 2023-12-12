from django.db import transaction
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from api.models import Product
from api.permissions import IsAdmin
from api.serializers.product import ProductSerializer


class ProductView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated, IsAdmin]

        return super(ProductView, self).get_permissions()

    @transaction.atomic
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Product.objects.filter(status=Product.ProductStatus.ACTIVE)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'

    def get_object(self):
        product = Product.objects.filter(status=Product.ProductStatus.ACTIVE) \
            .filter(id=self.kwargs[self.lookup_field])
        obj = get_object_or_404(product)

        return obj

