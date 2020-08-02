from django.db import transaction
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import (
    viewsets,
    status
)
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tenants.filters import TenantFilter
from tenants.models import (
    Tenant,
    Organization,
    Project,
)
from tenants.permissions import (
    TenantPermission,
    IsOrganizationMemberPermission,
    IsOrganizationOwnerPermission,
    IsOrganizationAdminOrOwnerPermission,
    IsOwnOrganization,
)
from tenants.schema import OrganizationInviteSchema
from tenants.serializers import (
    TenantSerializer,
    OrganizationThinSerializer,
    OrganizationSerializer,
    OrganizationInviteSerializer,
    OrganizationProfileSerializer,
    OrganizationPromotionSerializer,
    OrganizationDemotionSerializer,
    ProjectSerializer,
)


class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsOwnOrganization,)

    def get_queryset(self):
        qs = super().get_queryset()

        if self.action == 'list':
            organization_id = self.request.GET.get('organization_id')
            if organization_id is None:
                raise ValidationError(
                    detail={'detail': 'project_id is required'},
                )
            qs = qs.filter(organization=organization_id)
        return qs


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    filter_class = TenantFilter

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
        elif self.action in ('destroy', 'member_promotion', 'member_demotion'):
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
        elif self.action == "member_demotion":
            return OrganizationDemotionSerializer
        elif self.action == "profile":
            return OrganizationProfileSerializer
        return OrganizationSerializer

    def list(self, request, *args, **kwargs):
        # We scope organizations list to only the requesting user's organizations
        tenant = request.user.tenant
        queryset = tenant.organizations.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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

    @action(detail=True, methods=['POST'], url_path='member-demotion')
    def member_demotion(self, request, pk=None):
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
