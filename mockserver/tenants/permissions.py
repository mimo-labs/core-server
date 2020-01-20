from rest_framework import permissions


class TenantPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user_ptr == request.user


class OrganizationPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.users.filter(pk=request.user.tenant.pk).exists()
