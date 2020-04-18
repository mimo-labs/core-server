from rest_framework import viewsets

from mocks.filters import MockFilterSet
from mocks.models import (
    Mock,
    HeaderType,
    HttpVerb,
    Category,
    Endpoint,
    Header
)
from mocks.permissions import IsOwnOrganization
from mocks.serializers import (
    MockSerializer,
    HeaderTypeSerializer,
    HttpVerbSerializer,
    CategorySerializer,
    EndpointSerializer,
    HeaderSerializer
)


class MockViewset(viewsets.ModelViewSet):
    queryset = Mock.objects.all()
    serializer_class = MockSerializer
    permission_classes = (IsOwnOrganization,)
    filter_class = MockFilterSet


class HeaderTypeViewset(viewsets.ModelViewSet):
    queryset = HeaderType.objects.all()
    serializer_class = HeaderTypeSerializer
    permission_classes = (IsOwnOrganization,)


class HeaderViewset(viewsets.ModelViewSet):
    queryset = Header.objects.all()
    serializer_class = HeaderSerializer
    permission_classes = (IsOwnOrganization,)


class HttpVerbViewset(viewsets.ModelViewSet):
    queryset = HttpVerb.objects.all()
    serializer_class = HttpVerbSerializer
    permission_classes = (IsOwnOrganization,)


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsOwnOrganization,)


class EndpointViewset(viewsets.ModelViewSet):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer
    permission_classes = (IsOwnOrganization,)
