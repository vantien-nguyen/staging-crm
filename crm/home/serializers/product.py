from rest_framework import serializers

from home.models import Product
from home.serializers.partner import PartnerSerializer


class ProductSerializer(serializers.ModelSerializer):
    partner = PartnerSerializer()

    class Meta:
        model = Product
        fields = ["id", "name", "description", "typology", "partner"]
