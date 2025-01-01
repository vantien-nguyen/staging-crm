from typing import Any

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.models import File, Partner
from home.permissions import GroupPermission
from home.serializers import PartnerSerializer
from home.utils import delete_file, upload_file


class PartnerViewSet(ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    authentication_classes = [JWTAuthentication]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = request.data
        if Partner.objects.filter(siren=data.get("siren", "")).exists():
            return Response(
                {"message": "Partner siren existed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        partner = Partner.objects.create(
            name=data.get("name", ""),
            description=data.get("description", ""),
            siren=data.get("siren", ""),
            code_postal=data.get("code_postal", ""),
            turnover=data.get("turnover", 0),
            cash=data.get("cash", 0),
            website=data.get("website", ""),
            typology=data.get("typology", ""),
            iban=data.get("iban", ""),
            bic=data.get("bic", '"'),
        )

        file = request.FILES.get("file", None)
        if file:
            url = upload_file(file)
            partner.file = File.objects.create(
                name=file.name,
                url=url,
                size=file.size,
                mime_type=file.content_type,
            )
            partner.save()

        return Response(PartnerSerializer(partner).data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        partner = self.get_object()
        data = request.data

        partner.name = data.get("name", "")
        partner.description = data.get("description", "")
        partner.siren = data.get("siren", "")
        partner.code_postal = data.get("code_postal", "")
        partner.turnover = data.get("turnover", 0)
        partner.cash = data.get("cash", 0)
        partner.website = data.get("website", "")
        partner.typology = data.get("typology", "")
        partner.iban = data.get("iban", "")
        partner.bic = data.get("bic", "")

        file = request.FILES.get("file", None)
        deleted_file = partner.file

        if file:
            url = upload_file(file)
            if deleted_file:
                deleted_file.delete()

            partner.file = File.objects.create(
                name=file.name,
                url=url,
                size=file.size,
                mime_type=file.content_type,
            )

        if not file and deleted_file:
            delete_file(deleted_file)
            deleted_file.delete()
            partner.file = None

        partner.save()

        return Response(
            {"message": "Partner updated."},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        partner = self.get_object()

        deleted_file = partner.file
        if deleted_file:
            delete_file(deleted_file)
            deleted_file.delete()

        partner.delete()
        return Response(
            {"message": "Partner deleted"}, status=status.HTTP_204_NO_CONTENT
        )
