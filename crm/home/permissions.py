from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class GroupPermission(BasePermission):
    """
    Custom permission to check if a user belongs to specific groups.
    """

    def has_permission(self, request: Request, view: viewsets.ModelViewSet) -> bool:
        rules = settings.PERMISSION_RULES

        basename = getattr(view, "basename", None)
        if basename in rules:
            allowed_actions = rules[basename].get(request.user.role, [])
            return view.action in allowed_actions

        return False
