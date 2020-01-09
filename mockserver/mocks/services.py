from django.http import (
    Http404,
)

from common.services import Service
from mocks.models import Mock


class MockService(Service):
    model = Mock.objects

    @classmethod
    def get_tenant_mocks(cls, organization, route, verb, params):
        try:
            mock = Mock.objects.get(
                organization=organization,
                path__path__startswith=route,
                verb__name=verb,
                is_active=True
            )
        except Mock.DoesNotExist:
            return None

        if params != mock.params.content:
            raise Http404()

        return mock
