from django.core.exceptions import ValidationError

from mocks.models import (
    Project
)
from tenants.models import (
    Organization
)


def hostname_from_request(request):
    return (
        request.get_host().split('.')[0].lower(),  # Organization
        request.get_host().split('.')[1].lower(),  # Project
    )


def organization_from_request(request):
    uuid = hostname_from_request(request)[0]
    try:
        return Organization.objects.get(
            uuid=uuid
        )
    except (Organization.DoesNotExist, ValidationError):
        return None


def project_from_request(request):
    project_name = hostname_from_request(request)[1]
    try:
        return Project.objects.get(
            name=project_name
        )
    except (Project.DoesNotExist, ValidationError):
        return None
