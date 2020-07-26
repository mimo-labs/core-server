from rest_framework import viewsets

from mocks.filters import (
    MockFilterSet,
    CategoryFilterSet,
)
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
    IsOwnProjectOrganization,
)


class MockViewset(viewsets.ModelViewSet):
    queryset = Mock.objects.all()
    serializer_class = MockSerializer
    permission_classes = (IsOwnProjectOrganization,)
    filter_class = MockFilterSet

    def get_queryset(self):
        qs = super().get_queryset()

        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            category_qs = Category.objects.filter(project_id=project_id)
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


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_class = CategoryFilterSet


class EndpointViewset(viewsets.ModelViewSet):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            category_qs = Category.objects.filter(project_id=project_id)
            qs = qs.filter(categories__in=category_qs)

        return qs
