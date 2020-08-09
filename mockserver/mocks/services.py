from django.http import (
    Http404,
)

from common.services import Service
from mocks.models import Mock, Endpoint, Category
from tenants.models import Project


class EndpointService(Service):
    model = Endpoint.objects

    @classmethod
    def get_endpoint_by_name_and_project(cls, path_name: str, project_id: int) -> Endpoint:
        project = Project.objects.get(id=project_id)
        categories = project.category_set.all()

        endpoint, created = cls.model.get_or_create(
            path=path_name,
            categories__in=categories
        )

        if created:
            uncategorized = categories.get(name='Uncategorized')  # TODO: extract to constant
            endpoint.categories.add(uncategorized)
            endpoint.save()

        return endpoint


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
                is_active=True,
                is_complete=True,
            )
        except Mock.DoesNotExist:
            return None

        mock_params = mock.params.first().content

        if params != mock_params:
            raise Http404()

        return mock
