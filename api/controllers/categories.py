from django.db import transaction
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Category
from ..permissions import IsAdmin
from ..serializers.category import CategorySerializer


class CategoryView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_permissions(self):
        # Your logic should be all here
        if self.request.method == 'CREATE':
            self.permission_classes = [IsAuthenticated, IsAdmin]
        else:
            self.permission_classes = []

        return super(CategoryView, self).get_permissions()

    @transaction.atomic
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'

    def get_permissions(self):
        # Your logic should be all here
        if self.request.method == 'GET':
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated, IsAdmin]

        return super(CategoryDetailView, self).get_permissions()

    @transaction.atomic
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        main_category = self.get_object()
        categories = Category.objects.filter(parent=main_category)
        if categories.count() == 0:
            return super().delete(request, *args, **kwargs)

        error = {"category": ["Could Not Delete Parent Category"]}
        raise ValidationError(detail=error)

