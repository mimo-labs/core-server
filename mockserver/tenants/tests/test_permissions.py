from django.test import TestCase
from rest_framework.test import APIRequestFactory

from common.tests.mixins import MockTestMixin
from tenants.permissions import (
    TenantPermission,
    IsOrganizationMemberPermission,
    IsOrganizationOwnerPermission,
    IsOrganizationAdminPermission
)


class TenantPermissionTestCase(MockTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.permission = TenantPermission()
        cls.tenant = cls.create_bare_minimum_tenant()
        cls.user = cls.tenant.user_ptr
        cls.factory = APIRequestFactory()

    def test_tenant_owner_user_is_allowed(self):
        request = self.factory.delete('/some/url')
        request.user = self.user

        is_allowed = self.permission.has_object_permission(request, None, self.tenant)

        self.assertTrue(is_allowed)


class OrganizationPermissionTestCase(MockTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.permission = IsOrganizationMemberPermission()
        cls.tenant = cls.create_bare_minimum_tenant()
        cls.organization = cls.create_bare_minimum_organization(cls.tenant)
        cls.factory = APIRequestFactory()

    # TODO: Once models are improved tighten up permission checking
    def test_tenant_in_organization_is_allowed(self):
        request = self.factory.delete('/some/url')
        request.user = self.tenant.user_ptr

        is_allowed = self.permission.has_object_permission(request, None, self.organization)

        self.assertTrue(is_allowed)


class OrganizationOwnerPermissionTestCase(MockTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.permission = IsOrganizationOwnerPermission()
        cls.tenant = cls.create_bare_minimum_tenant()
        cls.organization = cls.create_bare_minimum_organization(cls.tenant)
        cls.factory = APIRequestFactory()

    def test_tenant_flagged_as_owner_is_allowed(self):
        membership = self.organization.organizationmembership_set.get(tenant=self.tenant)
        membership.is_owner = True
        membership.save()
        request = self.factory.delete('/some/url')
        request.user = self.tenant.user_ptr

        is_allowed = self.permission.has_object_permission(request, None, self.organization)

        self.assertTrue(is_allowed)


class OrganizationAdminPermissionTestCase(MockTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.permission = IsOrganizationAdminPermission()
        cls.tenant = cls.create_bare_minimum_tenant()
        cls.organization = cls.create_bare_minimum_organization(cls.tenant)
        cls.factory = APIRequestFactory()

    def test_tenant_flagged_as_owner_is_allowed(self):
        membership = self.organization.organizationmembership_set.get(tenant=self.tenant)
        membership.is_admin = True
        membership.save()
        request = self.factory.delete('/some/url')
        request.user = self.tenant.user_ptr

        is_allowed = self.permission.has_object_permission(request, None, self.organization)

        self.assertTrue(is_allowed)
