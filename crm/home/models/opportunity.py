from decimal import Decimal

from django.db import models

from home.models import File, TimeStampMixin
from users.models import User


class TransferType(models.TextChoices):
    ONE_TIME = "One-Time", "One-Time"
    RECURRING = "Recurring", "Recurring"


class Frequency(models.TextChoices):
    MONTHLY = "Monthly", "Monthly"
    QUARTERLY = "Quarterly", "Quarterly"
    ANNUALLY = "Annually", "Annually"


class OpportunityStatus(models.TextChoices):
    INTEREST = "Interest", "Interest"
    AGREED_CLIENT = "Agreed-Client", "Agreed-Client"
    AGREED_PARTNER = "Agreed-Partner", "Agreed-Partner"
    SUCCESSFUL = "Successful", "Successful"
    UNSUCCESSFUL = "Unsuccessful", "Unsuccessful"


class Opportunity(TimeStampMixin):
    nominal = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal("0.00")
    )
    margin = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal("0.00")
    )
    status = models.CharField(
        max_length=20,
        choices=OpportunityStatus.choices,
        default=OpportunityStatus.INTEREST,
        null=True,
        blank=True,
    )
    transfer_type = models.CharField(
        max_length=20, choices=TransferType.choices, default=TransferType.RECURRING
    )
    frequency = models.CharField(
        max_length=20,
        choices=Frequency.choices,
        default=Frequency.MONTHLY,
        null=True,
        blank=True,
    )
    amount = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal("0.00")
    )
    maturity = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    sous_jacent = models.CharField(max_length=64, null=True)
    coupon_payments = models.CharField(max_length=64, null=True)
    rates = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    traab = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    capital_protection = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal("0.00")
    )
    coupon_protection = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal("0.00")
    )
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_created=True)
    contact = models.ForeignKey("Contact", models.CASCADE, related_name="opportunities")
    product = models.ForeignKey("Product", models.CASCADE, related_name="opportunities")
    user = models.ForeignKey(User, models.CASCADE, related_name="opportunities")
    file = models.OneToOneField(
        File,
        on_delete=models.CASCADE,
        related_name="opportunities",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "opportunities"
