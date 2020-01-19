from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from tenants.models import Tenant
from tenants.permissions import TenantPermission
from tenants.serializers import TenantSerializer


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = (TenantPermission,)

    @action(detail=False, methods=['get', ])
    def me(self, request):
        tenant = request.user.tenant
        serializer = self.serializer_class(tenant)

        return JsonResponse(serializer.data)
