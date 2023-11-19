from django.db import models

from .mixins import ModifiedByMixin


class Color(ModifiedByMixin):

    title = models.CharField(
        max_length=128,
        unique=True,
        null=False,
        blank=False,
    )
    code = models.CharField(
        max_length=128,
        unique=True,
        null=False,
        blank=False,
    )
    slug = models.SlugField(
        unique=True,
        allow_unicode=True,
        null=False,
        blank=False,
    )

    class Meta:
        db_table = 'color'
        verbose_name = 'Color'
        verbose_name_plural = 'Color'
