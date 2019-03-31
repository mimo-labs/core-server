import json

from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

from core.models import Mock
from core.serializers import MockSerializer

# Create your views here.


class MockViewset(viewsets.ModelViewSet):
    queryset = Mock.objects.all()
    serializer_class = MockSerializer


@csrf_exempt
def fetch_mock(request):
    try:
        existing = Mock.objects.get(path=request.path, verb=request.method)
    except Mock.DoesNotExist:
        raise Http404()
    content = json.loads(existing.content)
    status_code = int(existing.status_code)
    return JsonResponse(content, status=status_code, safe=False)
