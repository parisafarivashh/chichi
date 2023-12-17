from django.db import models

from . import Product
from .mixins import ModifiedByMixin


class Comment(ModifiedByMixin):

    body = models.CharField(
        max_length=128,
        unique=True,
        null=False,
        blank=False,
    )
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'authorize.User',
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    product = models.ForeignKey(
        Product,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    removed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'comment'
        verbose_name = 'comment'
        verbose_name_plural = 'Comment'

