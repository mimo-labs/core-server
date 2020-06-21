import logging

from common import constants
from common.services import Service
from tenants.models import Organization
from mocks.models import (
    HttpVerb,
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
