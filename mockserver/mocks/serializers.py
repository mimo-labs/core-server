from rest_framework import serializers

from mocks.models import (
    Mock,
    HeaderType,
    HttpVerb,
    Category,
    Endpoint,
    Header,
    Content,
    Params,
)
from mocks.services import EndpointService
from tenants.models import (
    Organization,
    Project,
)


class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Header
        fields = (
            'header_type',
            'value',
        )
        extra_kwargs: {
            'mock': {
                'write_only': True
            }
        }


class HeaderMockSerializer(serializers.ModelSerializer):
    header_type = serializers.CharField(source="header_type.name")

    class Meta:
        model = Header
        fields = (
            'header_type',
            'value',
        )
        read_only_fields = (
            'header_type',
            'value',
        )


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = (
            'content',
        )


class ParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Params
        fields = (
            'content',
        )


class MockSerializer(serializers.ModelSerializer):
    path = serializers.CharField(allow_null=True, required=False, default=None)
    verb = serializers.PrimaryKeyRelatedField(
        queryset=HttpVerb.objects.all(),
        allow_null=True,
        required=False,
    )

    # read fields
    content = serializers.SerializerMethodField()
    params = serializers.SerializerMethodField()
    headers = HeaderMockSerializer(many=True, read_only=True)

    # write fields
    mock_content = serializers.JSONField(write_only=True, required=False, default=dict)
    mock_params = serializers.JSONField(write_only=True, required=False, default=dict)
    mock_headers = HeaderSerializer(write_only=True, many=True, required=False)
    project_id = serializers.CharField(allow_null=True, write_only=True, source='project')

    def create(self, validated_data):
        headers = validated_data.pop('mock_headers', [])
        content = validated_data.pop('mock_content')
        params = validated_data.pop('mock_params')
        path_name = validated_data.pop('path')
        project_id = validated_data.pop('project')

        if path_name:
            # TODO: re-filling validated_data seems dirty. Investigate a better way
            validated_data['path'] = EndpointService.get_endpoint_by_name_and_project(
                path_name,
                project_id
            )

        mock = Mock.objects.create(**validated_data)

        for header in headers:
            Header.objects.create(
                mock=mock,
                **header
            )

        if content:
            mock_content = mock.content.get()
            mock_content.content = content
            mock_content.save()

        if params:
            mock_params = mock.params.get()
            mock_params.content = params
            mock_params.save()

        return mock

    def get_content(self, obj):
        return obj.content.get().content

    def get_params(self, obj):
        return obj.params.get().content

    class Meta:
        model = Mock
        depth = 1
        fields = (
            'id',
            'title',
            'path',
            'verb',
            'status_code',
            'is_active',
            'mock_headers',
            'mock_content',
            'mock_params',
            'content',
            'params',
            'headers',
            'project_id',
        )
        read_only_fields = (
            'content',
            'params',
            'headers',
        )


class HeaderTypeSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        allow_null=False
    )

    class Meta:
        model = HeaderType
        fields = (
            'id',
            'name',
            'organization',
        )


class HttpVerbSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        allow_null=False
    )

    class Meta:
        model = HttpVerb
        fields = (
            'id',
            'name',
            'organization',
        )


class CategorySerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), allow_null=False)

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'project',
        )


class EndpointSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        allow_null=False,
        many=True,
    )

    class Meta:
        model = Endpoint
        fields = (
            'id',
            'path',
            'categories',
        )

    def validate(self, data):
        # Endpoint Unicity:
        # Since all categories correspond to the same project
        # We can grab whichever. The first one is picked since it's guaranteed to exist
        project = data['categories'][0].project
        project_categories = project.category_set.all()

        for category in project_categories:
            category_endpoints = category.endpoints.all()
            if any(ep for ep in category_endpoints if ep.path == data['path']):
                raise serializers.ValidationError(
                    "An endpoint with the path %s already exists for the project." % data['path']
                )

        return data
