from rest_framework import permissions


class IsOwnOrganization(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:  # Requires login
            return False

        return obj.organization_id in [
            org.id for
            org in
            request.user.tenant.organizations.all()
        ]
