from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet


class TenantPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: GenericViewSet):
        # Allow registering access
        if view.action == 'create':
            return True

        # Require authentication
        if request.user.is_anonymous:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        return obj.user_ptr == request.user
