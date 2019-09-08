import json

from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

from core.models import Mock
from core.serializers import MockSerializer


class MockViewset(viewsets.ModelViewSet):
    queryset = Mock.objects.all()
    serializer_class = MockSerializer


@csrf_exempt  # This allows verbs besides GET
def fetch_mock(request):
    query_params = {**request.GET.dict(), **request.POST.dict()}
    mock_route = request.path.rstrip('/')
    matching_mock = None
    existing = Mock.objects.filter(
        path__startswith=mock_route,
        verb__name=request.method
    )

    if not any(existing):
        raise Http404()

    if len(existing) == 1:
        matching_mock = existing.first()
    else:
        for mock in existing:
            # trim line breaks and whitespace
            mock_params = json.loads(mock.params)

            if query_params == mock_params:
                matching_mock = mock
                break
        else:
            raise Http404()

    content = json.loads(matching_mock.content)
    status_code = int(matching_mock.status_code)

    response = JsonResponse(
        content,
        status=status_code,
        safe=False
    )
    for header in matching_mock.header_set.all():
        header_type, value = header.as_response_header
        response[header_type] = value

    return response
