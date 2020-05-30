from rest_framework import permissions


class IsOwnOrganization(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:  # Requires login
            return False

        if view.action != 'list':
            return True

        organization_id = int(request.query_params.get('organization'))

        return organization_id in [
            org.id for
            org in
            request.user.tenant.organizations.all()
        ]

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:  # Requires login
            return False

        return obj.organization_id in [
            org.id for
            org in
            request.user.tenant.organizations.all()
        ]


class IsOwnProjectOrganization(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:  # Requires login
            return False

        if view.action != 'list':
            return True

        organization_id = int(request.query_params.get('organization'))

        return organization_id in [
            org.id for
            org in
            request.user.tenant.organizations.all()
        ]

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:  # Requires login
            return False

        return obj.project.organization_id in [
            org.id for
            org in
            request.user.tenant.organizations.all()
        ]
