import logging

from rest_framework import permissions


logger = logging.getLogger(__name__)


class IsOrganizationTenantPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.organization is None:
            logger.warning('non-existent organization requested')
            return False

        return request.organization.users.filter(
            email=request.user.email
        ).exists()
