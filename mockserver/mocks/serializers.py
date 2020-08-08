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
    path = serializers.PrimaryKeyRelatedField(queryset=Endpoint.objects.all(), allow_null=True)
    verb = serializers.PrimaryKeyRelatedField(queryset=HttpVerb.objects.all(), allow_null=True)

    headers = HeaderSerializer(many=True)
    mock_content = serializers.JSONField(write_only=True)
    mock_params = serializers.JSONField(write_only=True)

    def create(self, validated_data):
        headers = validated_data.pop('headers')
        content = validated_data.pop('mock_content')
        params = validated_data.pop('mock_params')

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

    class Meta:
        model = Mock
        depth = 1
        fields = (
            'title',
            'path',
            'verb',
            'status_code',
            'is_active',
            'mock_content',
            'mock_params',
            'content',
            'params',
            'headers',
        )
        read_only_fields = (
            'content',
            'params',
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
