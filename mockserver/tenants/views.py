from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from tenants.models import (
    Tenant,
    Organization
)
from tenants.permissions import (
    TenantPermission,
    IsOrganizationMemberPermission,
    IsOrganizationOwnerPermission,
    IsOrganizationAdminOrOwnerPermission
)
from tenants.serializers import (
    TenantSerializer,
    OrganizationThinSerializer,
    OrganizationSerializer
)


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = (IsAuthenticated, TenantPermission,)

    @action(detail=False, methods=['get', ])
    def me(self, request):
        tenant = request.user.tenant
        serializer = self.serializer_class(tenant)

        return JsonResponse(serializer.data)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [IsAuthenticated()]
        elif self.action == 'retrieve':
            return [IsAuthenticated(), IsOrganizationMemberPermission()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsOrganizationOwnerPermission()]
        else:
            return [
                IsAuthenticated(),
                IsOrganizationAdminOrOwnerPermission()
            ]

    def get_serializer_class(self):
        if self.action == 'list':
            return OrganizationThinSerializer
        return OrganizationSerializer
