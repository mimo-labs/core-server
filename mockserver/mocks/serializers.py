from rest_framework import serializers

from mocks.models import Mock, HeaderType, HttpVerb


class MockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mock
        fields = (
            'title',
            'path',
            'verb',
            'status_code',
            'is_active',
            'tenant',
        )


class HeaderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderType
        fields = (
            'name',
            'tenant',
        )


class HttpVerbSerializer(serializers.ModelSerializer):
    class Meta:
        model = HttpVerb
        fields = (
            'name',
            'tenant',
        )
