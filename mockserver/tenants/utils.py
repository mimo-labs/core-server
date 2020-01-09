from django.core.exceptions import ValidationError

from tenants.models import (
    Organization
)


def hostname_from_request(request):
    return request.get_host().split(':')[0].lower()


def organization_from_request(request):
    hostname = hostname_from_request(request)
    tenant_prefix = hostname.split('.')[0]
    try:
        return Organization.objects.get(
            uuid=tenant_prefix
        )
    except (Organization.DoesNotExist, ValidationError):
        return None
