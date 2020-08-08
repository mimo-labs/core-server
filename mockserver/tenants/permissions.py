from rest_framework import permissions, exceptions

from tenants.models import (
    Organization,
    OrganizationMembership,
    Project,
)


class IsOwnOrganization(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:  # Requires login
            return False

        if view.action != 'list':
            return True

        organization_id = request.query_params.get('organization_id')

        # Propagate the missing id to fail later on
        if organization_id is None:
            return True

        # Propagate if the organization doesn't exist. this is handled
        # by the views
        if Organization.objects.filter(id=organization_id).count() < 1:
            return True

        return int(organization_id) in [
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


class IsOwnProject(permissions.BasePermission):
    def has_permission(self, request, view):
        # This permission handles the case for list and create requests
        # The problem is, django sends data for both on separate objects
        # one of them being an abstraction over dicts that interpretes query params
        # as lists, regardless of syntax. So we need its underlying dict
        data = {**request.data, **request.query_params.dict()}
        project_id = data.get('project_id')

        # In case no project id, we let it go through and fail later
        # TODO: Is this right here? review viewset execution order
        if not project_id:
            return True

        if not Project.objects.filter(id=project_id).exists():
            raise exceptions.NotFound(
                detail="project does not exist",
            )

        tenant = request.user.tenant
        for org in tenant.organizations.all():
            if project_id in [str(proj.id) for proj in org.project_set.all()]:
                return True

        return False

    def has_object_permission(self, request, view, obj):
        object_organization = obj.project.organization
        tenant = request.user.tenant

        return object_organization in tenant.organizations.all()
