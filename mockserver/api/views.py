import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from authentication.decorators.tenant_view import tenancy_required
from mocks.models import Content
from mocks.services import MockService


@csrf_exempt  # This allows verbs besides GET
@tenancy_required
def fetch_mock(request):
    query_params = {**request.GET.dict(), **request.POST.dict()}
    mock_route = request.path.rstrip('/')

    mock = MockService.get_tenant_mocks(request.tenant, mock_route, request.method, query_params)

    try:
        content = json.loads(mock.content)
    except Content.DoesNotExist:
        content = {}
    status_code = mock.status_code

    response = JsonResponse(
        content,
        status=status_code,
        safe=False
    )
    for header in mock.header_set.all():
        header_type, value = header.as_response_header
        response[header_type] = value

    return response
