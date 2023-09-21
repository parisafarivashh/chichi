from django.db import models

from ..mixins import ModifiedByMixin


class Color(ModifiedByMixin):
    title = models.CharField(max_length=128)
    code = models.CharField(max_length=128)

    class Meta:
        db_table = 'color'
        verbose_name = "Color"
        verbose_name_plural = "Color"

