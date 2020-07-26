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
            qs = qs.filter(path__categories__in=category_qs)
            if not qs.exists():
                raise NotFound(
                    detail='project does not exist',
                )

        return qs


class HeaderTypeViewset(viewsets.ModelViewSet):
    queryset = HeaderType.objects.all()
    serializer_class = HeaderTypeSerializer
    permission_classes = (IsOwnOrganization,)


class HttpVerbViewset(viewsets.ModelViewSet):
    queryset = HttpVerb.objects.all()
    serializer_class = HttpVerbSerializer
    permission_classes = (IsOwnOrganization,)


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
            qs = qs.filter(project_id=project_id)
            if not qs.exists():
                raise NotFound(
                    detail='project does not exist',
                )

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
            qs = qs.filter(categories__in=category_qs)
            if not qs.exists():
                raise NotFound(
                    detail='project does not exist',
                )

        return qs
