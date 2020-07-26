from django_filters import rest_framework as filters

from mocks.models import Mock, Category


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


class CategoryFilterSet(filters.FilterSet):
    project_id = filters.NumberFilter(
        field_name="project",
        required=True,
    )

    class Meta:
        model = Category
        fields = [
            'project',
        ]
