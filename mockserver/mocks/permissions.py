from rest_framework import permissions

from tenants.models import Organization


class IsOwnOrganization(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:  # Requires login
            return False

        organization_id = request.data['organization']

        try:
            organization = Organization.objects.get(id=organization_id)
            return request.user.tenant in organization.users.all()
        except Organization.DoesNotExist:
            return False
