from rest_framework import viewsets

from mocks.filters import MockFilterSet
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
    permission_classes = (IsOwnProjectOrganization,)


class EndpointViewset(viewsets.ModelViewSet):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer
    permission_classes = (IsOwnProjectOrganization,)
