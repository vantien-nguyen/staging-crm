from rest_framework import serializers

from home.models import Kyc
from home.serializers.file import FileSerializer
from users.serializers import UserSerializer


class KycSerializer(serializers.ModelSerializer):
    assignee = UserSerializer()
    kbis = FileSerializer(many=True)
    certified_statuses = FileSerializer(many=True)
    tax_returns = FileSerializer(many=True)

    class Meta:
        model = Kyc
        fields = [
            "id",
            "name",
            "status",
            "notes",
            "der",
            "qcf",
            "kbis",
            "certified_statuses",
            "tax_returns",
            "assignee",
        ]
