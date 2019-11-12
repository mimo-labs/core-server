import json

from django.http import Http404
from django.shortcuts import get_object_or_404

from base.services import Service
from mocks.models import Mock


class MocksFetchService(Service):
    model = Mock.objects

    @classmethod
    def get_tenant_mocks(cls, tenant, route, verb, params):
        mock = get_object_or_404(
            Mock,
            tenant=tenant,
            path__startswith=route,
            verb__name=verb,
            is_active=True
        )

        # trim line breaks and whitespace
        mock_params = json.loads(mock.params)

        if params != mock_params:
            raise Http404()
