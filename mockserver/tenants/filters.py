from django_filters import rest_framework as filters

from tenants.models import Tenant


class TenantFilter(filters.FilterSet):
    organization_id = filters.NumberFilter(field_name="organizations", required=True)

    class Meta:
        model = Tenant
        fields = [
            'organization_id',
        ]
