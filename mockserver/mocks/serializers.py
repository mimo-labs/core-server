from rest_framework import serializers

from mocks.models import (
    Mock,
    HeaderType,
    HttpVerb,
    Category,
    Endpoint,
    Header
)


class MockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mock
        fields = (
            'title',
            'path',
            'verb',
            'status_code',
            'is_active',
            'organization',
        )


class HeaderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderType
        fields = (
            'name',
            'organization',
        )


class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Header
        fields = (
            'organization',
            'header_type',
            'value',
            'mock',
        )


class HttpVerbSerializer(serializers.ModelSerializer):
    class Meta:
        model = HttpVerb
        fields = (
            'name',
            'organization',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'organization',
        )


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = (
            'organization',
            'path',
            'category',
        )
