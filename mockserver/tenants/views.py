from django.db import transaction
from django.http import JsonResponse
from rest_framework import (
    viewsets,
    status
)
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
    OrganizationSerializer,
    OrganizationInviteSerializer
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
        elif self.action == "member-invite":
            return OrganizationInviteSerializer
        return OrganizationSerializer

    @transaction.atomic
    @action(detail=True, methods=['POST'], url_path='member-invite')
    def member_invite(self, request, pk=None):
        organization = self.get_object()

        for email in request.data['emails']:
            try:
                tenant = Tenant.objects.get(email=email)
            except Tenant.DoesNotExist:
                tenant = None
            data = {
                'organization': organization,
                'email': email,
                'tenant': tenant,
            }

            ser = self.get_serializer(data=data)
            ser.is_valid(raise_exception=True)
            ser.save()

        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
