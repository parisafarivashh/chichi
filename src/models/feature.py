from django.db import models


class Feature(models.Model):
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='features'
    )
    json = models.JSONField()

    class Meta:
        db_table = 'feature'
        verbose_name = "Feature"
        verbose_name_plural = "Feature"

