from typing import Any

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.models import Account, Contact, File
from home.permissions import GroupPermission
from home.serializers import ContactSerializer
from home.utils import delete_file, get_object_or_none, upload_file


class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["account_id"]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = request.data
        if Contact.objects.filter(email=data.get("email", "")).exists():
            return Response(
                {"message": "Contact email existed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        contact = Contact.objects.create(
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            phone_number=data.get("phone_number", ""),
            email=data.get("email", ""),
            linkedin=data.get("linkedin", ""),
            job_description=data.get("job_description", ""),
            account=get_object_or_none(Account, pk=request.data["account"]),
        )

        file = request.FILES.get("file", None)
        if file:
            url = upload_file(file)
            contact.file = File.objects.create(
                name=file.name,
                url=url,
                size=file.size,
                mime_type=file.content_type,
            )
            contact.save()

        return Response(ContactSerializer(contact).data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        contact = self.get_object()
        data = request.data

        contact.first_name = data.get("first_name", "")
        contact.last_name = data.get("last_name", "")
        contact.phone_number = data.get("phone_number", "")
        contact.linkedin = data.get("linkedin", "")
        contact.job_description = data.get("job_description", "")
        contact.account = get_object_or_none(Account, pk=data.get("account", None))

        file = request.FILES.get("file", None)
        deleted_file = contact.file

        if file:
            if deleted_file:
                delete_file(deleted_file)
                deleted_file.delete()

            url = upload_file(file)
            contact.file = File.objects.create(
                name=file.name,
                url=url,
                size=file.size,
                mime_type=file.content_type,
            )

        if not file and deleted_file:
            delete_file(deleted_file)
            deleted_file.delete()
            contact.file = None

        contact.save()

        return Response(
            {"message": "Contact updated."},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        contact = self.get_object()

        deleted_file = contact.file
        if deleted_file:
            delete_file(deleted_file)
            deleted_file.delete()

        contact.delete()
        return Response(
            {"message": "Contact deleted"}, status=status.HTTP_204_NO_CONTENT
        )
