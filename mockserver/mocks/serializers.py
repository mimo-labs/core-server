from rest_framework import serializers

from mocks.models import (
    Mock,
    HeaderType,
    HttpVerb,
    Category,
    Endpoint,
    Header,
    Project,
    Content,
    Params,
)
from tenants.models import Organization


class ProjectSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        allow_null=False
    )

    class Meta:
        model = Project
        fields = (
            'name',
            'organization',
        )


class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Header
        fields = (
            'header_type',
            'value',
            'mock',
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
    path = serializers.PrimaryKeyRelatedField(queryset=Endpoint.objects.all(), allow_null=False)
    verb = serializers.PrimaryKeyRelatedField(queryset=HttpVerb.objects.all(), allow_null=False)

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
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=False)

    class Meta:
        model = Endpoint
        fields = (
            'id',
            'path',
            'category',
        )
