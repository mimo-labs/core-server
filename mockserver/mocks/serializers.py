from rest_framework import serializers

from mocks.models import Mock, HeaderType, HttpVerb


class MockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mock
        fields = '__all__'


class HeaderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderType
        fields = '__all__'


class HttpVerbSerializer(serializers.ModelSerializer):
    class Meta:
        model = HttpVerb
        fields = '__all__'
