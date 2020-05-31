from rest_framework import permissions

from tenants.models import (
    Organization,
    OrganizationMembership
)


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


class TenantPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user_ptr == request.user


class IsOrganizationMemberPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Organization):
        return obj.users.filter(pk=request.user.tenant.pk).exists()


class IsOrganizationOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Organization):
        try:
            return obj.organizationmembership_set.get(
                tenant=request.user.tenant
            ).is_owner
        except OrganizationMembership.DoesNotExist:
            return False


class IsOrganizationAdminPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Organization):
        try:
            return obj.organizationmembership_set.get(
                tenant=request.user.tenant
            ).is_admin
        except OrganizationMembership.DoesNotExist:
            return False


class IsOrganizationAdminOrOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, *args):
        return (
            IsOrganizationOwnerPermission().has_object_permission(*args)
            or IsOrganizationAdminPermission().has_object_permission(*args)
        )
