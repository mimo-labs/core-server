import json

from django.http import Http404
from django.shortcuts import get_object_or_404

from base.services import Service
from mocks.models import Mock, Params


class MocksFetchService(Service):
    model = Mock.objects

    @classmethod
    def get_tenant_mocks(cls, tenant, route, verb, params):
        mock = get_object_or_404(
            Mock,
            tenant=tenant,
            path__path__startswith=route,
            verb__name=verb,
            is_active=True
        )

        import ipdb; ipdb.set_trace()
        # trim line breaks and whitespace
        try:
            mock_params = json.loads(mock.params)
        except Params.DoesNotExist:
            mock_params = {}

        if params != mock_params:
            raise Http404()

        return mock
