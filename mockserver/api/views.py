import logging

from django.http import JsonResponse
from rest_framework.decorators import (
    permission_classes,
    api_view
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_404_NOT_FOUND

from api.permissions import (
    IsOrganizationTenantPermission
)
from authentication.decorators.tenant_view import tenancy_required
from mocks.services import MockService


logger = logging.getLogger(__name__)


@tenancy_required
@api_view(('GET', 'POST', 'PUT', 'PATCH', 'DELETE'))
@permission_classes((IsAuthenticated & IsOrganizationTenantPermission,))
def fetch_mock(request):
    logger.info(f'fetch_mock organization {request.organization.uuid}')

    query_params = {**request.GET.dict(), **request.POST.dict(), **request.data}
    mock_route = request.path.rstrip('/')

    endpoint = MockService.get_mock_endpoint(mock_route, request.project)

    mock = MockService.get_tenant_mocks(
        request.project,
        endpoint,
        request.method,
        query_params
    )

    if mock is None:
        logger.info(f'mock not found organization {request.organization.uuid}')
        return JsonResponse(
            {'detail': 'mock does not exist'},
            status=HTTP_404_NOT_FOUND
        )

    content = mock.content.get()

    response = JsonResponse(
        content.content,
        status=mock.status_code,
        safe=False
    )
    for header in mock.headers.all():
        header_type, value = header.as_response_header
        response[header_type] = value

    logger.info(f'end fetch_mock organization {request.organization.uuid}')
    return response
