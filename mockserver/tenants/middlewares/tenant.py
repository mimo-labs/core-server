from django.core.exceptions import ValidationError

from tenants.models import Tenant
from tenants.utils import tenant_from_request


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            tenant_uuid = tenant_from_request(request)
            request.tenant = tenant_uuid
        except (Tenant.DoesNotExist, ValidationError):
            request.tenant = None

        response = self.get_response(request)
        return response
