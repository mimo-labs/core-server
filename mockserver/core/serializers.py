from core.models import Mock
from rest_framework import serializers


class MockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mock
        fields = '__all__'
