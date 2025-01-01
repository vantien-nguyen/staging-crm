from decimal import Decimal

from django.db import models

from home.models import TimeStampMixin


class Billing(TimeStampMixin):
    reason = models.TextField()
    amount = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal("0.00")
    )
    billing_date = models.DateTimeField(auto_created=True)
    opportunity = models.ForeignKey(
        "Opportunity", models.CASCADE, related_name="billings"
    )
    partner = models.ForeignKey("Partner", models.CASCADE, related_name="billings")
    file = models.OneToOneField(
        "File", on_delete=models.CASCADE, related_name="billing", null=True, blank=True
    )

    class Meta:
        db_table = "billings"

    @property
    def client_name(self) -> str:
        if not self.opportunity.contact:
            return ""

        return self.opportunity.contact.account.name

    @property
    def partner_name(self) -> str:
        if not self.partner:
            return ""

        return self.partner.name
