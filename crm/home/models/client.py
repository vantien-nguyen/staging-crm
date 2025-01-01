from django.contrib.postgres.fields import ArrayField
from django.db import models

from home.models import Account


class ClientStatus(models.TextChoices):
    CLIENT = "Client", "Client"
    PROSPECT = "Prospect", "Prospect"


class Client(Account):
    status = models.CharField(
        max_length=20, choices=ClientStatus.choices, default=ClientStatus.CLIENT
    )
    needs = ArrayField(
        base_field=models.CharField(max_length=1000, null=True), null=True, blank=True
    )
    existing_partners = ArrayField(
        base_field=models.CharField(max_length=1000, null=True), null=True, blank=True
    )

    class Meta:
        db_table = "clients"
