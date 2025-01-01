from rest_framework import serializers

from home.models import Billing


class BillingSerializer(serializers.ModelSerializer):
    partner_name = serializers.ReadOnlyField()
    client_name = serializers.ReadOnlyField()

    class Meta:
        model = Billing
        fields = ["reason", "amount", "billing_date", "client_name", "partner_name"]
