from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from base.serializers import TechnologySerializer
from tenants.models import (
    Tenant,
    Organization,
    OrganizationMembership,
    OrganizationInvite,
    OrganizationProfile
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


class OrganizationProfileSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(read_only=True, many=True)

    class Meta:
        model = OrganizationProfile
        fields = (
            'public_name',
            'description',
            'avatar',
            'technologies',
            'website',
            'twitter',
            'facebook',
            'linkedin',
            'instagram',
        )


class OrganizationSerializer(serializers.ModelSerializer):
    users = TenantSerializer(many=True, required=False)
    member_count = serializers.ReadOnlyField()
    mock_count = serializers.ReadOnlyField()
    profile = OrganizationProfileSerializer(required=False)

    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
            'uuid',
            'is_playground',
            'users',
            'profile',
            'member_count',
            'mock_count',
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
            'from_domain',
        )
