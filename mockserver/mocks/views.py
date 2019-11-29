from rest_framework import viewsets

from mocks.models import Mock, HeaderType, HttpVerb
from mocks.serializers import MockSerializer, HeaderTypeSerializer, HttpVerbSerializer
# Create your views here.


class MockViewset(viewsets.ModelViewSet):
    queryset = Mock.objects.all()
    serializer_class = MockSerializer


class HeaderTypeViewset(viewsets.ModelViewSet):
    queryset = HeaderType.objects.all()
    serializer_class = HeaderTypeSerializer


class HttpVerbViewset(viewsets.ModelViewSet):
    queryset = HttpVerb.objects.all()
    serializer_class = HttpVerbSerializer
