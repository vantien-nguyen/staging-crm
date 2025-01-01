from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from home.views import (
    AccountViewSet,
    BillingViewSet,
    ClientViewSet,
    ContactViewSet,
    DashboardViewSet,
    InteractionViewSet,
    KycViewSet,
    OpportunityViewSet,
    PartnerViewSet,
    ProductViewSet,
    health,
)

router = routers.DefaultRouter()
router.register(r"dashboard", DashboardViewSet, basename="dashboard")
router.register(r"accounts", AccountViewSet, basename="accounts")
router.register(r"billings", BillingViewSet, basename="billings")
router.register(r"contacts", ContactViewSet, basename="contacts")
router.register(r"clients", ClientViewSet, basename="clients")
router.register(r"interactions", InteractionViewSet, basename="interactions")
router.register(r"kycs", KycViewSet, basename="kycs")
router.register(r"opportunities", OpportunityViewSet, basename="opportunities")
router.register(r"partners", PartnerViewSet, basename="partners")
router.register(r"products", ProductViewSet, basename="products")

urlpatterns = [
    path("", include(router.urls)),
    path("health", health),
    # path(
    #     "google/files/upload/",
    #     upload_files_to_google_drive,
    #     name="upload_files_to_google_drive",
    # ),
]
