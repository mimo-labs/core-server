from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from base.serializers import TechnologySerializer
from tenants.models import (
    Tenant,
    Organization,
    OrganizationMembership,
    OrganizationInvite,
    OrganizationProfile,
    Project,
)


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


class OrganizationProfileThinSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationProfile
        fields = (
            'public_name',
            'avatar',
        )


class OrganizationThinSerializer(serializers.ModelSerializer):
    profile = OrganizationProfileThinSerializer()

    class Meta:
        depth = 1
        model = Organization
        fields = (
            'uuid',
            'profile',
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


class TenantSerializer(serializers.ModelSerializer):
    organizations = OrganizationThinSerializer(many=True, read_only=True)

    class Meta:
        model = Tenant
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'password',
            'organizations',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value: str):
        return make_password(value)


class OrganizationSerializer(serializers.ModelSerializer):
    users = TenantSerializer(many=True, read_only=True)
    profile = OrganizationProfileSerializer(read_only=True)
    member_count = serializers.ReadOnlyField()
    mock_count = serializers.ReadOnlyField()

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


class OrganizationPromotionSerializer(serializers.Serializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all())
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())

    class Meta:
        fields = ('tenant', 'organization',)

    def validate(self, attrs):
        if not OrganizationMembership.objects.filter(
            tenant=attrs['tenant'],
            organization=attrs['organization']
        ).exists():
            raise serializers.ValidationError('tenant is not part of the organization')

        return attrs

    def create(self, validated_data):
        membership = OrganizationMembership.objects.get(
            tenant=validated_data['tenant'],
            organization=validated_data['organization']
        )
        membership.is_admin = True
        membership.save()

        return membership
