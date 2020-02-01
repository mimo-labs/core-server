from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from tenants.models import (
    Tenant,
    Organization,
    OrganizationMembership,
    OrganizationInvite
)


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value: str):
        return make_password(value)


class OrganizationThinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
            'uuid',
        )


class OrganizationSerializer(serializers.ModelSerializer):
    users = TenantSerializer(many=True, required=False)

    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
            'uuid',
            'is_playground',
            'users'
        )
        read_only_fields = (
            'is_playground',
            'users',
        )

    def create(self, validated_data):
        organization = super(OrganizationSerializer, self).create(validated_data)

        tenant = self.context['request'].user.tenant
        membership = OrganizationMembership(
            tenant=tenant,
            organization=organization,
            is_owner=True,
            is_admin=True
        )
        membership.save()

        return organization


class OrganizationInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationInvite
        fields = (
            'organization',
            'email',
            'tenant',
        )
