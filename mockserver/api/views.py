import json

from django.http import JsonResponse
from rest_framework import viewsets

from core.models import Mock
from core.serializers import MockSerializer

# Create your views here.


class MockViewset(viewsets.ModelViewSet):
    queryset = Mock.objects.all()
    serializer_class = MockSerializer


def fetch_mock(request):
    existing = Mock.objects.get(path=request.path)
    content = json.loads(existing.content)
    status_code = int(existing.status_code)
    return JsonResponse(content, status=status_code, safe=False)
