from rest_framework import serializers

from base.models import Technology


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = (
            'code',
            'name',
        )
