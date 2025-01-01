from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.models import Billing
from home.permissions import GroupPermission
from home.serializers import BillingSerializer


class BillingViewSet(ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    authentication_classes = [JWTAuthentication]
