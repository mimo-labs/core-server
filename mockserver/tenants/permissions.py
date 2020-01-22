from rest_framework import permissions

from tenants.models import (
    Organization,
    OrganizationMembership
)


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
