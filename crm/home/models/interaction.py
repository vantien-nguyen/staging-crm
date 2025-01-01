from django.db import models

from home.models import TimeStampMixin
from users.models import User


class InteractionType(models.TextChoices):
    CALL = "Call", "Call"
    MAIL = "Mail", "Mail"
    APPOINTMENT = "Appointment", "Appointment"
    VISUAL = "Visual", "Visual"


class InteractionStatus(models.TextChoices):
    PLANED = "Planed", "Planed"
    DONE = "Done", "Done"
    CANCELED = "Canceled", "Canceled"


class Interaction(TimeStampMixin):
    date_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=InteractionStatus.choices,
        default=InteractionStatus.PLANED,
    )
    type = models.CharField(
        max_length=20, choices=InteractionType.choices, default=InteractionType.CALL
    )
    comment = models.TextField(null=True)
    user = models.ForeignKey(User, models.CASCADE, related_name="interactions")
    contact = models.ForeignKey("Contact", models.CASCADE, related_name="interactions")

    class Meta:
        db_table = "interactions"
