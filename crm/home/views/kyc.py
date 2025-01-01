from typing import Any

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.models import File, FileStatus, Kyc, KycStatus
from home.permissions import GroupPermission
from home.serializers import KycSerializer
from home.utils import delete_file, get_object_or_none, upload_file
from users.models import User


class KycViewSet(ModelViewSet):
    queryset = Kyc.objects.all()
    serializer_class = KycSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    authentication_classes = [JWTAuthentication]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = request.data
        kyc = Kyc.objects.create(
            name=data.get("name", ""),
            status=data.get("status", KycStatus.PENDING),
            notes=data.get("notes", ""),
            der=True if data.get("der", "") == "true" else False,
            qcf=True if data.get("qcf", "") == "true" else False,
            assignee=get_object_or_none(User, pk=data.get("assignee", None)),
        )

        self.upload_files(kyc, "kbis", request.FILES)
        self.upload_files(kyc, "certified_statuses", request.FILES)
        self.upload_files(kyc, "tax_returns", request.FILES)

        return Response(KycSerializer(kyc).data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        kyc = self.get_object()
        data = request.data

        kyc.name = data.get("name", kyc.name)
        kyc.status = data.get("status", kyc.status)
        kyc.notes = data.get("notes", kyc.notes)
        kyc.der = data.get("der", "false").lower() == "true"
        kyc.qcf = data.get("qcf", "false").lower() == "true"
        kyc.assignee = get_object_or_none(User, pk=data.get("assignee", None))

        self.update_files(kyc, "kbis", request.FILES)
        self.update_files(kyc, "certified_statuses", request.FILES)
        self.update_files(kyc, "tax_returns", request.FILES)

        kyc.save()

        return Response(KycSerializer(kyc).data, status=status.HTTP_200_OK)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        kyc = self.get_object()

        self.delete_files(kyc, "kbis")
        self.delete_files(kyc, "certified_statuses")
        self.delete_files(kyc, "tax_returns")

        kyc.delete()

        return Response({"message": "Kyc deleted"}, status=status.HTTP_204_NO_CONTENT)

    def delete_files(self, kyc: Kyc, field_name: str):
        existing_files = getattr(kyc, field_name).all()
        for existing_file in existing_files:
            if existing_file:
                delete_file(existing_file)
                existing_file.delete()

    def update_files(self, kyc: Kyc, field_name: str, files: Request.FILES):
        existing_files = getattr(kyc, field_name).all()
        new_files = files.getlist(f"{field_name}[]")

        if new_files:
            for existing_file in existing_files:
                if existing_file:
                    delete_file(existing_file)
                    existing_file.delete()

            for file in new_files:
                url = upload_file(file)
                file_instance = File.objects.create(
                    name=file.name,
                    url=url,
                    size=file.size,
                    mime_type=file.content_type,
                    status=FileStatus.SUCCESS,
                )
                kyc_files = getattr(kyc, field_name)
                kyc_files.add(file_instance)

        elif not new_files:
            for existing_file in existing_files:
                if existing_file:
                    delete_file(existing_file)
                    existing_file.delete()

    def upload_files(self, kyc: Kyc, field_name: str, files: Request.FILES):
        file_list = files.getlist(f"{field_name}[]")
        if file_list:
            for file in file_list:
                url = upload_file(file)
                file_instance = File.objects.create(
                    name=file.name,
                    url=url,
                    size=file.size,
                    mime_type=file.content_type,
                    status=FileStatus.SUCCESS,
                )
                kyc_files = getattr(kyc, field_name)
                kyc_files.add(file_instance)
            kyc.save()
