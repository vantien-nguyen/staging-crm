from rest_framework import serializers

from home.models import Interaction
from home.serializers.contact import ContactSerializer
from users.serializers import UserSerializer


class InteractionSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    user = UserSerializer()

    class Meta:
        model = Interaction
        fields = ["id", "status", "date_time", "type", "comment", "contact", "user"]
