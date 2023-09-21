from django.db import models

from ..mixins import ModifiedByMixin


class Discount(ModifiedByMixin):
    name = models.CharField(max_length=255)
    variant = models.ForeignKey(
        'Variant', on_delete=models.CASCADE, related_name='disconnects'
    )
    modifier_type = models.CharField(
        max_length=10,
        choices=[
            ('discount', 'Discount'),
            ('surcharge', 'Surcharge')
        ]
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    modifier_value = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'disconnect'
        verbose_name = "Disconnect"
        verbose_name_plural = "Disconnect"
