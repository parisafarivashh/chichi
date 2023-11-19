from django.db import transaction
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Category
from ..permissions import IsAdmin
from ..serializers.category import CategorySerializer


class CategoryView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = CategorySerializer

    @transaction.atomic
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'

    @transaction.atomic
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        main_category = self.get_object()
        categories = Category.objects.filter(parent=main_category)
        serializer = self.serializer_class(instance=categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        main_category = self.get_object()
        categories = Category.objects.filter(parent=main_category)
        if categories.count == 0:
            return super().delete(request, *args, **kwargs)

        error = {"category": ["Could Not Delete Parent Category"]}
        raise ValidationError(detail=error)

