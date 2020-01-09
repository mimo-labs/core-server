import logging

from django.http import JsonResponse
from rest_framework.status import HTTP_404_NOT_FOUND


logger = logging.getLogger(__name__)


def tenancy_required(fn):
    def wrap(request, *args, **kwargs):
        if request.organization is None:
            return JsonResponse(
                {'detail': 'organization does not exist'},
                status=HTTP_404_NOT_FOUND
            )
        return fn(request, *args, **kwargs)
    return wrap
