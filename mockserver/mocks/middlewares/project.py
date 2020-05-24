from tenants.utils import project_from_request

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed


class ProjectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        if settings.IS_ADMIN_API:
            raise MiddlewareNotUsed()

    def __call__(self, request):
        request.project = project_from_request(request)

        response = self.get_response(request)
        return response
