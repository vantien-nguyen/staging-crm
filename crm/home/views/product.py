from typing import Any

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.models import Partner, Product
from home.permissions import GroupPermission
from home.serializers import ProductSerializer
from home.utils import get_object_or_none


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    authentication_classes = [JWTAuthentication]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = request.data

        product = Product.objects.create(
            name=data.get("name", ""),
            description=data.get("description", ""),
            typology=data.get("typology", ""),
            partner=get_object_or_none(Partner, pk=data.get("partner", None)),
        )

        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        product = self.get_object()
        data = request.data

        product.name = data.get("name", "")
        product.description = data.get("description", "")
        product.typology = data.get("typology", "")
        product.partner = get_object_or_none(Partner, pk=data.get("partner", None))
        product.save()

        return Response(
            {"message": "Product updated."},
            status=status.HTTP_200_OK,
        )
