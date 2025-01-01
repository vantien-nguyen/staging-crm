from typing import Any

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.models import (
    Contact,
    File,
    Frequency,
    Opportunity,
    OpportunityStatus,
    Product,
)
from home.permissions import GroupPermission
from home.serializers import OpportunitySerializer
from home.utils import delete_file, get_object_or_none, upload_file
from users.models import User


class OpportunityViewSet(ModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    authentication_classes = [JWTAuthentication]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = request.data
        opportunity = Opportunity.objects.create(
            nominal=data.get("nominal", 0),
            margin=data.get("margin", 0),
            status=data.get("status", OpportunityStatus.INTEREST),
            frequency=data.get("frequency", Frequency.MONTHLY),
            amount=data.get("amount", 0),
            maturity=data.get("maturity", 0),
            sous_jacent=data.get("sous_jacent", ""),
            coupon_payments=data.get("coupon_payments", ""),
            rates=data.get("rates", 0),
            traab=data.get("traab", 0),
            capital_protection=data.get("capital_protection", 0),
            coupon_protection=data.get("coupon_protection", 0),
            start_date=data.get("start_date", ""),
            end_date=data.get("end_date", ""),
            created_date=data.get("created_date", ""),
            contact=get_object_or_none(Contact, pk=data.get("contact", None)),
            product=get_object_or_none(Product, pk=data.get("product", None)),
            user=get_object_or_none(User, pk=data.get("user", None)),
        )

        file = request.FILES.get("file", None)
        if file:
            url = upload_file(file)
            opportunity.file = File.objects.create(
                name=file.name,
                url=url,
                size=file.size,
                mime_type=file.content_type,
            )
            opportunity.save()

        return Response(
            OpportunitySerializer(opportunity).data, status=status.HTTP_201_CREATED
        )

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        opportunity = self.get_object()
        data = request.data

        opportunity.nominal = data.get("nominal", 0)
        opportunity.margin = data.get("margin", 0)
        opportunity.status = data.get("status", OpportunityStatus.INTEREST)
        opportunity.frequency = data.get("frequency", Frequency.MONTHLY)
        opportunity.amount = data.get("amount", 0)
        opportunity.maturity = data.get("maturity", 0)
        opportunity.sous_jacent = data.get("sous_jacent", "")
        opportunity.coupon_payments = data.get("coupon_payments", "")
        opportunity.rates = data.get("rates", 0)
        opportunity.traab = data.get("traab", 0)
        opportunity.capital_protection = data.get("capital_protection", 0)
        opportunity.coupon_protection = data.get("coupon_protection", 0)
        opportunity.start_date = data.get("start_date", "")
        opportunity.end_date = data.get("end_date", "")
        opportunity.created_date = data.get("created_date", "")
        opportunity.contact = get_object_or_none(Contact, pk=data.get("contact", None))
        opportunity.product = get_object_or_none(Product, pk=data.get("product", None))
        opportunity.user = get_object_or_none(User, pk=data.get("user", None))

        file = request.FILES.get("file", None)
        deleted_file = opportunity.file

        if file:
            url = upload_file(file)
            if deleted_file:
                deleted_file.delete()

            opportunity.file = File.objects.create(
                name=file.name,
                url=url,
                size=file.size,
                mime_type=file.content_type,
            )

        if not file and deleted_file:
            delete_file(deleted_file)
            deleted_file.delete()
            opportunity.file = None

        opportunity.save()

        return Response(
            {"message": "Opportunity updated."},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        opportunity = self.get_object()

        deleted_file = opportunity.file
        if deleted_file:
            delete_file(deleted_file)
            deleted_file.delete()

        opportunity.delete()
        return Response(
            {"message": "Opportunity deleted"}, status=status.HTTP_204_NO_CONTENT
        )
