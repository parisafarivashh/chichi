from django.db import models

from ..mixins import ModifiedByMixin


class Product(ModifiedByMixin):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True, allow_unicode=True)
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='products'
    )

    class Meta:
        db_table = 'product'
        verbose_name = "Product"
        verbose_name_plural = "Products"

