import logging

from rest_framework import permissions


logger = logging.getLogger(__name__)


class IsOrganizationTenantPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.tenant is None:
            logger.warning('non-existent tenant requested')
            return False

        return request.tenant.users.filter(
            email=request.user.email
        ).exists()
