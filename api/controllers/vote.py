from django.db import transaction
from django.db.models import Sum, Count
from rest_framework import generics
from rest_framework.generics import get_object_or_404

from api.models import Vote, Product
from api.serializers import VoteSerializer


class VoteView(
    generics.ListCreateAPIView,
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()
    lookup_field = 'id'

    @transaction.atomic
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def perform_create(self, serializer):
        product = get_object_or_404(Product, id=self.kwargs.get('product_id'))
        serializer.save(created_by=self.request.user, product=product)
        rates = Vote.objects.filter(product_id=product.id) \
            .aggregate(sum_rate=Sum('rate'), count_vote=Count('id'))

        product.rate = rates['sum_rate'] / rates['count_vote']
        product.save(update_fields=['rate'])

