from tenants.utils import organization_from_request


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.organization = organization_from_request(request)

        response = self.get_response(request)
        return response
