from datetime import datetime

import pytz
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.models import Client, Interaction, Opportunity
from home.permissions import GroupPermission
from home.serializers import (
    ClientSerializer,
    DashboardRequestSerializer,
    InteractionSerializer,
    OpportunitySerializer,
)


class DashboardViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, GroupPermission]
    authentication_classes = [JWTAuthentication]

    def list(self, request: Request, *args, **kwargs) -> Response:

        serializer = DashboardRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        start_date = datetime.strptime(serializer.data["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(serializer.data["end_date"], "%Y-%m-%d")
        start_date = pytz.utc.localize(start_date)
        end_date = pytz.utc.localize(end_date).replace(hour=23, minute=59)

        type_ = serializer.data.get("type", "opportunity")
        models_maping = {
            "opportunity": Opportunity,
            "client": Client,
            "interaction": Interaction,
        }
        serializer_maping = {
            "opportunity": OpportunitySerializer,
            "client": ClientSerializer,
            "interaction": InteractionSerializer,
        }
        model = models_maping.get(type_)
        serializer_class = serializer_maping.get(type_)

        objects = model.objects.filter(created_at__range=(start_date, end_date)).all()
        data = serializer_class(objects, many=True).data

        return Response(data, status=status.HTTP_200_OK)
