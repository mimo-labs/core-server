import json

from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from core.models import Mock
from core.serializers import MockSerializer


class MockViewset(viewsets.ModelViewSet):
    queryset = Mock.objects.all()
    serializer_class = MockSerializer


@csrf_exempt  # This allows verbs besides GET
def fetch_mock(request):
    mock_route = request.path.rstrip('/')

    mock = get_object_or_404(
        Mock,
        path__startswith=mock_route,
        verb__name=request.method,
        is_active=True
    )

    # trim line breaks and whitespace
    mock_params = json.loads(mock.params)
    query_params = {**request.GET.dict(), **request.POST.dict()}

    if query_params != mock_params:
        raise Http404()

    response = JsonResponse(
        mock.content,
        status=mock. status_code,
        safe=False
    )

    for header in mock.header_set.all():
        header_type, value = header.as_response_header
        response[header_type] = value

    return response
