from unittest.mock import Mock

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import (
    APIRequestFactory,
    APITestCase,
)

from common.tests.mixins import MockTestMixin
from tenants.permissions import (
    TenantPermission,
    IsOrganizationMemberPermission,
    IsOrganizationOwnerPermission,
    IsOrganizationAdminPermission,
    IsOwnProjectOrganization,
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


class OrganizationMemberPermissionTestCase(MockTestMixin, TestCase):
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


class ProjectOrganizationPermissionTestCase(APITestCase, MockTestMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request_factory = APIRequestFactory()
        cls.permission_class = IsOwnProjectOrganization()
        cls.tenant = cls.create_bare_minimum_tenant()
        cls.organization = cls.create_bare_minimum_organization(cls.tenant)
        cls.token = cls.tenant.user_ptr.auth_token
        cls.url = reverse('v1:mock-list')

    def setUp(self):
        self.view = Mock()
        self.view.action = "list"

    def test_anonymous_user_is_denied(self):
        request = self.request_factory.get(self.url)
        request.user = AnonymousUser()

        allowed = self.permission_class.has_permission(request, self.view)

        self.assertFalse(allowed)

    def test_detail_request_is_allowed(self):
        detail_url = reverse("v1:mock-detail", kwargs={'pk': 1})
        request = self.request_factory.get(detail_url)
        request.user = self.tenant.user_ptr
        self.view.action = "retrieve"

        result = self.permission_class.has_permission(request, self.view)

        self.assertTrue(result)

    def test_accessing_mock_in_different_organization_is_denied(self):
        other_organization = self.create_bare_minimum_organization()
        request = self.request_factory.get(self.url)
        request.query_params = {'organization': other_organization.pk}
        request.user = self.tenant.user_ptr

        result = self.permission_class.has_permission(request, self.view)

        self.assertFalse(result)

    def test_user_included_in_organization_is_allowed(self):
        request = self.request_factory.get(self.url)
        request.query_params = {'organization': self.organization.pk}
        request.user = self.tenant.user_ptr

        result = self.permission_class.has_permission(request, self.view)

        self.assertTrue(result)


class ProjectOrganizationObjectPermissionTestCase(MockTestMixin, APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.permission_class = IsOwnProjectOrganization()
        cls.tenant = cls.create_bare_minimum_tenant()
        cls.organization = cls.create_bare_minimum_organization(cls.tenant)
        cls.request_factory = APIRequestFactory()
        cls.mock = cls.create_bare_minimum_mock(cls.tenant)
        cls.url = reverse('v1:mock-detail', kwargs={'pk': cls.mock.pk})

    def setUp(self):
        self.view = Mock()
        self.view.action = 'retrieve'

    def test_anonymous_user_is_denied(self):
        request = self.request_factory.get(self.url)
        request.user = AnonymousUser()

        allowed = self.permission_class.has_object_permission(request, self.view, self.mock)

        self.assertFalse(allowed)

    def test_accessing_mock_in_different_organization_is_denied(self):
        other_mock = self.create_bare_minimum_mock()
        other_url = reverse('v1:mock-detail', kwargs={'pk': other_mock.pk})
        request = self.request_factory.get(other_url)
        request.user = self.tenant.user_ptr

        result = self.permission_class.has_object_permission(request, self.view, other_mock)

        self.assertFalse(result)

    def test_user_included_in_organization_is_allowed(self):
        request = self.request_factory.get(self.url)
        request.user = self.tenant.user_ptr

        result = self.permission_class.has_object_permission(request, self.view, self.mock)

        self.assertTrue(result)
