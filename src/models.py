from django.db import models

from .mixins import ModifiedByMixin


class Category(ModifiedByMixin):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, allow_unicode=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(ModifiedByMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True, allow_unicode=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='categories'
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class PriceModifier(ModifiedByMixin):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='price_modifiers'
    )
    modifier_type = models.CharField(
        max_length=10,
        choices=[
            ('discount', 'Discount'),
            ('surcharge', 'Surcharge')
        ]
    )
    condition_attribute = models.ForeignKey(
        'ProductAttribute', on_delete=models.SET_NULL, null=True, blank=True
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    modifier_value = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Product Modifier"
        verbose_name_plural = "Products Modifier"


class ProductAttribute(ModifiedByMixin):
    class AttributeTypeChoice(models.TextChoices):
        text = 'text'
        integer = 'integer'
        float = 'float'
        decimal = 'decimal'

    title = models.CharField(max_length=100)
    type = models.CharField(
        max_length=16,
        choices=AttributeTypeChoice.choices,
        default=AttributeTypeChoice.text
    )

    class Meta:
        verbose_name = "Product Attribute"
        verbose_name_plural = "Product Attribute"


class ProductAttributeValue(ModifiedByMixin):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_attribute_values',
    )
    attribute = models.ForeignKey(
        ProductAttribute, on_delete=models.CASCADE, related_name='attribute_values'
    )

    decimal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    text = models.TextField(blank=True, null=True)
    integer = models.IntegerField(null=True, blank=True)
    float = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Product Attribute Value"
        verbose_name_plural = "Product Attribute Values"
        unique_together = ('product', 'attribute')


class ProductVariation(ModifiedByMixin):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='variations'
    )
    attributes = models.ManyToManyField(ProductAttributeValue)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Product Variation"
        verbose_name_plural = "Product Variation"

