from rest_framework import viewsets

from mocks.models import Mock
from mocks.serializers import MockSerializer


class MockViewset(viewsets.ModelViewSet):
    queryset = Mock.objects.all()
    serializer_class = MockSerializer
