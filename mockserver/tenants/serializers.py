from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from tenants.models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value: str):
        return make_password(value)
