from unittest.mock import Mock

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from common.tests.mixins import MockTestMixin
from tenants.permissions import TenantPermission


class TenantPermissionTestCase(MockTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.permission = TenantPermission()
        cls.tenant = cls.create_bare_minimum_tenant()
        cls.user = cls.tenant.user_ptr
        cls.factory = APIRequestFactory()

    def test_create_request_is_allowed(self):
        view = Mock()
        view.action = 'create'

        is_allowed = self.permission.has_permission(None, view)

        self.assertTrue(is_allowed)

    def test_unauthenticated_user_is_denied(self):
        request = self.factory.post('/some/url')
        request.user = AnonymousUser()
        view = Mock()
        view.action = 'list'

        is_allowed = self.permission.has_permission(request, view)

        self.assertFalse(is_allowed)

    def test_authenticated_list_is_allowed(self):
        request = self.factory.get('/some/url')
        request.user = Mock()
        request.user.is_anonymous = False
        view = Mock()
        view.action = 'list'

        is_allowed = self.permission.has_permission(request, view)

        self.assertTrue(is_allowed)

    def test_unauthenticated_detail_permission_is_denied(self):
        request = self.factory.delete('/some/url')
        request.user = AnonymousUser()

        is_allowed = self.permission.has_object_permission(request, None, self.tenant)

        self.assertFalse(is_allowed)

    def test_tenant_owner_user_is_allowed(self):
        request = self.factory.delete('/some/url')
        request.user = self.user

        is_allowed = self.permission.has_object_permission(request, None, self.tenant)

        self.assertTrue(is_allowed)
