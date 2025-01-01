from django.db import models

from home.models import Account, File, TimeStampMixin


class Contact(TimeStampMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    job_description = models.TextField(null=True)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="contacts",
        null=True,
        blank=True,
    )
    file = models.OneToOneField(
        File, on_delete=models.CASCADE, related_name="contact", null=True, blank=True
    )

    class Meta:
        db_table = "contacts"

    @property
    def status(self) -> str:
        if not self.account:
            return ""

        return self.account.status if hasattr(self.account, "status") else "Partner"
