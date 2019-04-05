import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from core.models import Mock
from core.serializers import MockSerializer


class MockViewset(viewsets.ModelViewSet):
    queryset = Mock.objects.all()
    serializer_class = MockSerializer


@csrf_exempt  # Para permitir POST y otros verbos
def fetch_mock(request):
    existing = get_object_or_404(Mock, path=request.path, verb=request.method)
    content = json.loads(existing.content)
    status_code = int(existing.status_code)
    return JsonResponse(content, status=status_code, safe=False)
