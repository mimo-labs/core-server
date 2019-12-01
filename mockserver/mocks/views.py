from rest_framework import viewsets

from mocks.models import (
    Mock,
    HeaderType,
    HttpVerb,
    Category,
    Endpoint
)
from mocks.serializers import (
    MockSerializer,
    HeaderTypeSerializer,
    HttpVerbSerializer,
    CategorySerializer,
    EndpointSerializer
)


class MockViewset(viewsets.ModelViewSet):
    queryset = Mock.objects.all()
    serializer_class = MockSerializer


class HeaderTypeViewset(viewsets.ModelViewSet):
    queryset = HeaderType.objects.all()
    serializer_class = HeaderTypeSerializer


class HttpVerbViewset(viewsets.ModelViewSet):
    queryset = HttpVerb.objects.all()
    serializer_class = HttpVerbSerializer


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class EndpointViewset(viewsets.ModelViewSet):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer
