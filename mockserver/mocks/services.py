from django.http import (
    Http404,
)

from common.services import Service
from mocks.models import Mock, Endpoint, Category
from tenants.models import Project


class MockService(Service):
    model = Mock.objects

    @classmethod
    def get_mock_endpoint(cls, path: str, project: Project) -> Endpoint:
        # TODO: refactor? Does this belong here?
        project_categories = Category.objects.filter(project=project)
        return Endpoint.objects.get(
            path=path,
            categories__in=project_categories
        )

    @classmethod
    def get_tenant_mocks(
            cls,
            project: Project,
            path: Endpoint,
            verb: str,
            params: dict
    ) -> Mock:
        try:
            mock = Mock.objects.get(
                path=path,
                verb__name=verb,
                is_active=True
            )
        except Mock.DoesNotExist:
            return None

        mock_params = mock.params.first().content

        if params != mock_params:
            raise Http404()

        return mock
