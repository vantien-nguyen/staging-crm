from rest_framework import serializers

from home.models import Opportunity
from home.serializers.contact import ContactSerializer
from home.serializers.file import FileSerializer
from home.serializers.product import ProductSerializer
from users.serializers import UserSerializer


class OpportunitySerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    product = ProductSerializer()
    file = FileSerializer()
    user = UserSerializer()

    class Meta:
        model = Opportunity
        fields = [
            "id",
            "nominal",
            "margin",
            "status",
            "frequency",
            "amount",
            "maturity",
            "sous_jacent",
            "coupon_payments",
            "rates",
            "traab",
            "capital_protection",
            "coupon_protection",
            "start_date",
            "end_date",
            "created_date",
            "contact",
            "product",
            "user",
            "file",
        ]
