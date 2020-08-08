from rest_framework import viewsets
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated

from mocks.models import (
    Mock,
    HeaderType,
    HttpVerb,
    Category,
    Endpoint,
)
from mocks.serializers import (
    MockSerializer,
    HeaderTypeSerializer,
    HttpVerbSerializer,
    CategorySerializer,
    EndpointSerializer,
)
from tenants.models import Project
from tenants.permissions import (
    IsOwnOrganization,
    IsOwnProject,
)


class MockViewset(viewsets.ModelViewSet):
    queryset = Mock.objects.all()
    serializer_class = MockSerializer
    permission_classes = (IsAuthenticated, IsOwnProject)

    def get_queryset(self):
        qs = super().get_queryset()

        if self.action == 'list':
            project_id = self.request.GET.get('project_id')
            if project_id is None:
                raise ValidationError(
                    detail={'detail': 'project_id is required'},
                )
            category_qs = Category.objects.filter(project_id=project_id)
            # At least 1 category is always present for a project
            # If there isn't any, the project doesn't exist at all
            if not category_qs.exists():
                raise NotFound(
                    detail='project does not exist',
                )
            qs = qs.filter(path__categories__in=category_qs)
        return qs


class HeaderTypeViewset(viewsets.ModelViewSet):
    queryset = HeaderType.objects.all()
    serializer_class = HeaderTypeSerializer
    permission_classes = (IsOwnOrganization,)


class HttpVerbViewset(viewsets.ModelViewSet):
    queryset = HttpVerb.objects.all()
    serializer_class = HttpVerbSerializer
    permission_classes = (IsOwnOrganization,)

    def get_queryset(self):
        qs = super().get_queryset()

        if self.action == 'list':
            organization_id = self.request.GET.get('organization_id')
            if organization_id is None:
                raise ValidationError(
                    detail={'detail': 'organization_id is required'},
                )
            qs = qs.filter(organization_id=organization_id)
            # Verbs are mandatory and automatically bootstrapped for all orgs
            # so if none exist for a given org id, that organization doesn't exist
            if not qs.exists():
                raise NotFound(
                    detail='organization does not exist',
                )
        return qs


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, IsOwnProject,)

    def get_queryset(self):
        qs = super().get_queryset()

        if self.action == 'list':
            project_id = self.request.GET.get('project_id')
            if project_id is None:
                raise ValidationError(
                    detail={'detail': 'project_id is required'},
                )
            if Project.objects.filter(id=project_id).count() < 1:
                raise NotFound(
                    detail='project does not exist',
                )
            qs = qs.filter(project_id=project_id)
        return qs


class EndpointViewset(viewsets.ModelViewSet):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer
    permission_classes = (IsAuthenticated, IsOwnProject,)

    def get_queryset(self):
        qs = super().get_queryset()

        if self.action == 'list':
            project_id = self.request.GET.get('project_id')
            if project_id is None:
                raise ValidationError(
                    detail={'detail': 'project_id is required'},
                )
            category_qs = Category.objects.filter(project_id=project_id)
            # At least 1 category is always present for a project
            # If there isn't any, the project doesn't exist at all
            if not category_qs.exists():
                raise NotFound(
                    detail='project does not exist',
                )
            qs = qs.filter(categories__in=category_qs)
        return qs
