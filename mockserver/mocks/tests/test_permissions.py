from unittest.mock import (
    Mock,
    patch
)

from django.test import TestCase

from common.tests.mixins import MockTestMixin
from mocks.permissions import IsOwnOrganization
from tenants.models import Organization


class OrganizationPermissionTestCase(TestCase, MockTestMixin):
    @classmethod
    def setUpClass(cls):
        super(OrganizationPermissionTestCase, cls).setUpClass()
        cls.permission_class = IsOwnOrganization()

    def setUp(self):
        self.request = Mock()
        self.request.data = {
            'organization': '99999999999999999'
        }
        self.request.user = Mock()

    def test_anonymous_user_is_denied(self):
        self.request.user.is_anonymous = True

        allowed = self.permission_class.has_permission(self.request, None)

        self.assertFalse(allowed)

    @patch('tenants.models.Organization.objects')
    def test_non_existent_organization_is_denied(self, mock_org):
        mock_org.get.side_effect = Organization.DoesNotExist
        self.request.user.is_anonymous = False

        result = self.permission_class.has_permission(self.request, None)

        self.assertFalse(result)

    @patch('tenants.models.Organization.objects')
    def test_user_without_organization_is_denied(self, mock_org):
        self.request.user.is_anonymous = False
        organization = Organization.objects.create(
            name='foobar'
        )
        mock_org.get.return_value = organization

        result = self.permission_class.has_permission(self.request, None)

        self.assertFalse(result)

    def test_user_included_in_organization_is_allowed(self):
        tenant = self.create_bare_minimum_tenant()
        self.request.user = tenant
        self.request.data['organization'] = tenant.organization_set.first().id
        mock_org = Mock(wraps=Organization.objects)
        mock_org.get.return_value = tenant.organization_set.first()

        result = self.permission_class.has_permission(self.request, None)

        self.assertTrue(result)
