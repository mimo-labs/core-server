from django_filters import rest_framework as filters

from mocks.models import Mock


class MockFilterSet(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr='iexact'
    )
    verb = filters.CharFilter(
        field_name="verb__name",
        lookup_expr="iexact"
    )

    class Meta:
        model = Mock
        fields = [
            'title',
            'verb',
            'status_code',
        ]
