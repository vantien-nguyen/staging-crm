from typing import Any

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.models import Client, File
from home.permissions import GroupPermission
from home.serializers import ClientSerializer
from home.utils import delete_file, upload_file


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    authentication_classes = [JWTAuthentication]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = request.data
        if Client.objects.filter(siren=data.get("siren", "")).exists():
            return Response(
                {"message": "Client siren existed."}, status=status.HTTP_400_BAD_REQUEST
            )

        client = Client.objects.create(
            name=data.get("name", ""),
            description=data.get("description", ""),
            siren=data.get("siren", ""),
            code_postal=data.get("code_postal", ""),
            turnover=data.get("turnover", 0),
            cash=data.get("cash", 0),
            website=data.get("website", ""),
            typology=data.get("typology", ""),
            status=data.get("status", ""),
            # needs=data.get("typology", None),
            # existing_partners=data.get("typology", None),
        )

        file = request.FILES.get("file", None)
        if file:
            url = upload_file(file)
            client.file = File.objects.create(
                name=file.name,
                url=url,
                size=file.size,
                mime_type=file.content_type,
            )
            client.save()

        return Response(ClientSerializer(client).data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        client = self.get_object()
        data = request.data

        client.name = data.get("name", "")
        client.description = data.get("description", "")
        client.siren = data.get("siren", "")
        client.code_postal = data.get("code_postal", "")
        client.turnover = data.get("turnover", 0)
        client.cash = data.get("cash", 0)
        client.website = data.get("website", "")
        client.typology = data.get("typology", "")
        client.status = data.get("status", "")
        # client.needs = data.get("typology", [])
        # client.existing_partners = data.get("typology", [])

        file = request.FILES.get("file", None)
        deleted_file = client.file

        if file:
            url = upload_file(file)
            if deleted_file:
                deleted_file.delete()

            client.file = File.objects.create(
                name=file.name,
                url=url,
                size=file.size,
                mime_type=file.content_type,
            )

        if not file and deleted_file:
            delete_file(deleted_file)
            deleted_file.delete()
            client.file = None

        client.save()

        return Response(
            {"message": "Client updated."},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        client = self.get_object()

        deleted_file = client.file
        if deleted_file:
            delete_file(deleted_file)
            deleted_file.delete()

        client.delete()
        return Response(
            {"message": "Client deleted"}, status=status.HTTP_204_NO_CONTENT
        )
