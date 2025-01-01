from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from users.views import (
    CookieTokenBlacklistView,
    CookieTokenRefreshView,
    LogoutView,
    UserViewset,
    obtain_token_pairs,
)

app_name = "users"

router = routers.DefaultRouter()
router.register(r"", UserViewset, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/", obtain_token_pairs, name="auth_token"),
    path(
        "auth/token/refresh/",
        CookieTokenRefreshView.as_view(),
        name="auth_token_refresh",
    ),
    path(
        "auth/token/blacklist/",
        CookieTokenBlacklistView.as_view(),
        name="auth_token_blacklist",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
]
