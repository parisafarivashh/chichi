from django.db import models

from ..mixins import ModifiedByMixin


class Attribute(ModifiedByMixin):
    title = models.CharField(max_length=128)
    value = models.CharField(max_length=128)

    class Meta:
        db_table = 'attribute'
        verbose_name = "Attribute"
        verbose_name_plural = "Attribute"

