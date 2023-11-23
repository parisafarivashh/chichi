from django.db import models

from .color import Color
from .product import Product


class Variant(models.Model):

    class SizeTypeChoice(models.TextChoices):
        L = 'l'
        M = 'm'
        S = 's'
        xl = 'xl'
        xxl = 'xxl'

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='varients'
    )
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, related_name='varients'
    )
    size = models.CharField(
        max_length=16, choices=SizeTypeChoice.choices, null=True, blank=True
    )
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    count = models.IntegerField(default=0, null=False, blank=False)

    class Meta:
        db_table = 'variant'
        verbose_name = "Variant"
        verbose_name_plural = "Variant"

