from typing import Any

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.models import Contact, Interaction, InteractionStatus, User
from home.permissions import GroupPermission
from home.serializers import InteractionSerializer
from home.utils import get_object_or_none
from rest_framework.decorators import action

import logging

from django.apps import apps
from django.template.loader import get_template

from home.celery import app
from home.extensions import sendinblue

logger = logging.getLogger(__name__)

class InteractionViewSet(ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    authentication_classes = [JWTAuthentication]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = request.data

        interaction = Interaction.objects.create(
            date_time=data.get("date_time", ""),
            type=data.get("type", ""),
            status=data.get("status", InteractionStatus.PLANED),
            comment=data.get("comment", ""),
            contact=get_object_or_none(Contact, pk=data.get("contact", None)),
            user=get_object_or_none(User, pk=data.get("user", None)),
        )

        return Response(
            InteractionSerializer(interaction).data, status=status.HTTP_201_CREATED
        )

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        interaction = self.get_object()
        data = request.data

        interaction.date_time = data.get("date_time", "")
        interaction.type = data.get("type", "")
        interaction.status = data.get("status", InteractionStatus.PLANED)
        interaction.comment = data.get("comment", "")
        interaction.contact = get_object_or_none(Contact, pk=data.get("contact", None))
        interaction.user = get_object_or_none(User, pk=data.get("user", None))
        interaction.save()

        return Response(
            {"message": "Interaction updated."},
            status=status.HTTP_200_OK,
        )
    
    @action(
        detail=False,
        methods=["post"],
        url_name="send_der",
        url_path="send-der",
        permission_classes=[IsAuthenticated, GroupPermission],
        authentication_classes=[JWTAuthentication],
    )
    def send_der(self, request: Request) -> Response:
        target_emails = request.data.get("target_emails", [])

        html_content = get_template("mailing/der.html").render(
            {
            "user_first_name": "user_first_name",
        }
        )
        data = {
            "sender": {
                "name": "Tien",
                "email": "tiennguyenhust@gmail.com",
            },
            "to": [{"email":  "tiennguyenhust@gmail.com"}],
            "subject": "{} Bienvenue à rejoindre SEVE !".format(""),
            "htmlContent": html_content,
        }

        logger.info(
            "Sending referral invitation email",
            extra={"target_email": "test"},
        )
        sendinblue.send_email(data)

        return Response({"message": "Der sent."}, status=status.HTTP_201_CREATED)
    