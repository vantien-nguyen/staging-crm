import re

from django.core.exceptions import ValidationError
from django.db import models

from home.models import Account


def validate_iban(value):
    """Validates the format of an IBAN."""
    iban_pattern = re.compile(r"^[A-Z]{2}\d{2}[A-Z0-9]{4,30}$")
    if not iban_pattern.match(value):
        raise ValidationError("Invalid IBAN format.")


def validate_bic(value):
    """Validates the format of a BIC (SWIFT code)."""
    bic_pattern = re.compile(r"^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$")
    if not bic_pattern.match(value):
        raise ValidationError("Invalid BIC format.")


class Partner(Account):
    iban = models.CharField(
        max_length=34, validators=[validate_iban], blank=True, null=True
    )
    bic = models.CharField(
        max_length=34, validators=[validate_bic], blank=True, null=True
    )

    class Meta:
        db_table = "partners"
