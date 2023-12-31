from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Color
from ..permissions import IsAdmin
from ..serializers import ColorSerializer


class ColorView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = '__all__'
    lookup_field = 'slug'

