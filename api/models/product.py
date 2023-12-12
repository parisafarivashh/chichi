from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.constants import MAX_RATE, MIN_RATE
from api.models.mixins import ModifiedByMixin


class Product(ModifiedByMixin):

    class ProductStatus(models.TextChoices):
        ACTIVE = 'active'
        DEACTIVATED = 'deactivated'

    title = models.CharField(
        max_length=255,
        db_index=True,
        null=False,
        blank=False,
    )
    description = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )
    created_by = models.ForeignKey(
        'authorize.User',
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    rate = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(MAX_RATE),
            MinValueValidator(MIN_RATE),
        ]
    )
    status = models.CharField(
        choices=ProductStatus.choices,
        default=ProductStatus.ACTIVE,
    )

    class Meta:
        db_table = 'product'
        verbose_name = "Product"
        verbose_name_plural = "Products"

