from django.db import models

from home.models import File, TimeStampMixin
from users.models import User


class KycStatus(models.TextChoices):
    PENDING = "Pending", "Pending"
    COMPLETED = "Completed", "Completed"
    CANCELED = "Canceled", "Canceled"


class Kyc(TimeStampMixin):
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=KycStatus.choices, default=KycStatus.PENDING
    )
    notes = models.TextField(null=True)
    der = models.BooleanField(default=False)
    qcf = models.BooleanField(default=False)
    kbis = models.ManyToManyField(File, related_name="kyc_kbis", blank=True)
    certified_statuses = models.ManyToManyField(
        File, related_name="kyc_certified_statuses", blank=True
    )
    tax_returns = models.ManyToManyField(
        File, related_name="kyc_tax_returns", blank=True
    )
    assignee = models.ForeignKey(
        User, models.CASCADE, related_name="kycs", null=True, blank=True
    )

    class Meta:
        db_table = "kycs"
