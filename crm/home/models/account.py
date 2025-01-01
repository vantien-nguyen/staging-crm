from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from home.models.base import PolymorphicModelTimeStamp


def validate_siren(value):
    if len(value) != 9 or not value.isdigit():
        raise ValidationError("SIREN must be a 9-digit number.")


def validate_code_postal(value):
    if len(value) != 5 or not value.isdigit():
        raise ValidationError("Code Postal must be a 5-digit number.")


class Account(PolymorphicModelTimeStamp):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    siren = models.CharField(max_length=9, unique=True, validators=[validate_siren])
    code_postal = models.CharField(max_length=5, validators=[validate_code_postal])
    turnover = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal("0.00")
    )
    cash = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    website = models.URLField(max_length=200, blank=True, null=True)
    typology = models.CharField(max_length=255)
    file = models.OneToOneField(
        "File", on_delete=models.CASCADE, related_name="account", null=True, blank=True
    )

    class Meta:
        db_table = "accounts"
