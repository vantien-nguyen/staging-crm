from rest_framework import serializers

from home.models import Client
from home.serializers.file import FileSerializer


class ClientSerializer(serializers.ModelSerializer):
    file = FileSerializer()

    class Meta:
        model = Client
        fields = "__all__"
