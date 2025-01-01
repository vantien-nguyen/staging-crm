from django.db import models
from polymorphic.models import PolymorphicModel


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class PolymorphicModelTimeStamp(PolymorphicModel):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class FileStatus(models.TextChoices):
    UPLOADING = "Uploading", "Uploading"
    SUCCESS = "Success", "Success"
    FAILED = "Failed", "Failed"


class File(TimeStampMixin):
    name = models.CharField(max_length=128)
    url = models.URLField(blank=True, null=True)
    size = models.PositiveIntegerField()
    mime_type = models.CharField(max_length=64, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=FileStatus.choices, default=FileStatus.UPLOADING
    )

    class Meta:
        db_table = "files"

    def __str__(self):
        return self.name
