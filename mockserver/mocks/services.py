import json

from django.http import Http404

from base.services import Service
from mocks.models import Mock


class MocksFetchService(Service):
    model = Mock.objects

    @classmethod
    def get_by_route_and_verb(cls, route, verb, params):
        existing = Mock.objects.filter(
            path__startswith=route,
            verb__name=verb
        )

        if not any(existing):
            raise Http404()

        if len(existing) == 1:
            matching_mock = existing.first()
        else:
            for mock in existing:
                # trim line breaks and whitespace
                mock_params = json.loads(mock.params)

                if params == mock_params:
                    matching_mock = mock
            else:
                raise Http404()

        return matching_mock
