from django.db import models

from home.models import TimeStampMixin


class Product(TimeStampMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    typology = models.CharField(max_length=255, null=True, blank=True)
    partner = models.ForeignKey(
        "Partner", models.CASCADE, related_name="products", null=True
    )

    class Meta:
        db_table = "products"
