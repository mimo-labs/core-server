from django.db import transaction
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
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
from tenants.schema import OrganizationInviteSchema
from tenants.serializers import (
    TenantSerializer,
    OrganizationThinSerializer,
    OrganizationSerializer,
    OrganizationInviteSerializer,
    OrganizationProfileSerializer,
    OrganizationPromotionSerializer
)


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

    def get_permissions(self):
        if self.action == 'create':
            return (TenantPermission(),)
        return (IsAuthenticated(), TenantPermission(),)

    @action(detail=False, methods=['GET', ])
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
        elif self.action in ('destroy', 'member_promotion'):
            return [IsAuthenticated(), IsOrganizationOwnerPermission()]
        else:
            return [
                IsAuthenticated(),
                IsOrganizationAdminOrOwnerPermission()
            ]

    def get_serializer_class(self):
        if self.action == 'list':
            return OrganizationThinSerializer
        elif self.action == "member_invite":
            return OrganizationInviteSerializer
        elif self.action == "member_promotion":
            return OrganizationPromotionSerializer
        elif self.action == "profile":
            return OrganizationProfileSerializer
        return OrganizationSerializer

    @transaction.atomic
    @swagger_auto_schema(method='post', request_body=OrganizationInviteSchema,
                         responses={204: None})
    @action(detail=True, methods=['POST'], url_path='member-invite')
    def member_invite(self, request, pk=None):
        from_domain = request.META.get('HTTP_HOST')
        organization = self.get_object()

        for email in request.data['emails']:
            try:
                tenant = Tenant.objects.get(email=email)
            except Tenant.DoesNotExist:
                tenant = None
            data = {
                'organization': organization.pk,
                'email': email,
                'tenant': tenant,
                'from_domain': from_domain
            }

            ser = self.get_serializer(data=data)
            ser.is_valid(raise_exception=True)
            ser.save()

        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'], url_path='member-promotion')
    def member_promotion(self, request, pk=None):
        org = self.get_object()
        data = {
            **request.data,
            'organization': org.pk
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['PUT', 'PATCH'])
    def profile(self, request, pk=None):
        organization: Organization = self.get_object()

        serializer = self.get_serializer(organization.profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
