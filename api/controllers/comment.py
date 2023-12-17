from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from ..models import Comment, Product
from ..serializers.comment import CommentSerializer


class CommentView(
        generics.RetrieveUpdateDestroyAPIView,
        generics.ListCreateAPIView,
):
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = '__all__'
    search_fields = '__all__'
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def get_object(self):
        comment = Comment.objects \
            .filter(created_by=self.request.user) \
            .filter(product_id=self.kwargs['product_id']) \
            .filter(id=self.kwargs['id'])

        obj = get_object_or_404(comment)
        return obj

    def get_permissions(self):
        # Your logic should be all here
        if self.request.method == 'GET':
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated]

        return super(CommentView, self).get_permissions()

    @transaction.atomic
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_admin:
            return Comment.objects.all()
        return Comment.objects.filter(is_approved=True)

    def perform_create(self, serializer):
        try:
            product = Product.objects.get(id=self.kwargs.get('product_id'))
        except Product.DoesNotExist:
            raise NotFound
        serializer.save(created_by=self.request.user, product=product)

    def perform_update(self, serializer):
        try:
            product = Product.objects.get(id=self.kwargs.get('product_id'))
        except Product.DoesNotExist:
            raise NotFound
        serializer.save(created_by=self.request.user, product=product)

