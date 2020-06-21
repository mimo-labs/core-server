import logging

from common import constants
from common.services import Service
from tenants.models import Organization
from mocks.models import (
    HttpVerb,
    HeaderType,
)


logger = logging.getLogger(__name__)


class OrganizationService(Service):
    model = Organization

    @classmethod
    def bootstrap_organization(cls, organization: Organization):
        for verb in constants.STANDARD_VERBS:
            HttpVerb.objects.create(
                name=verb,
                organization=organization
            )

        for header_type in constants.STANDARD_HEADERS:
            HeaderType.objects.create(
                name=header_type,
                organization=organization
            )
