from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.constants import MAX_RATE, MIN_RATE
from api.models.mixins import ModifiedByMixin


class Vote(ModifiedByMixin):

    rate = models.IntegerField(
        null=False,
        blank=False,
        validators=[
            MaxValueValidator(MAX_RATE),
            MinValueValidator(MIN_RATE),
        ]
    )
    created_by = models.ForeignKey(
        'authorize.User',
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    product = models.ForeignKey(
        'api.Product',
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )

    class Meta:
        db_table = 'vote'
        verbose_name = 'vote'
        verbose_name_plural = 'votes'

