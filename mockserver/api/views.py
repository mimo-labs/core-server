from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_404_NOT_FOUND

from authentication.decorators.tenant_view import tenancy_required
from mocks.services import MockService


@csrf_exempt  # This allows verbs besides GET
@tenancy_required
def fetch_mock(request):
    query_params = {**request.GET.dict(), **request.POST.dict()}
    mock_route = request.path.rstrip('/')

    mock = MockService.get_tenant_mocks(request.tenant, mock_route, request.method, query_params)

    if mock is None:
        return JsonResponse(
            {'detail': 'mock does not exist'},
            status=HTTP_404_NOT_FOUND
        )

    response = JsonResponse(
        mock.content.content,
        status=mock.status_code,
        safe=False
    )
    for header in mock.header_set.all():
        header_type, value = header.as_response_header
        response[header_type] = value

    return response
