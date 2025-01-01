from rest_framework import serializers

from home.models import Contact
from home.serializers.account import AccountSerializer
from home.serializers.file import FileSerializer


class ContactSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()
    account = AccountSerializer()
    file = FileSerializer()

    class Meta:
        model = Contact
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "linkedin",
            "job_description",
            "status",
            "account",
            "file",
        ]
