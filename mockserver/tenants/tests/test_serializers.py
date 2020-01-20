from django.test import TestCase
from rest_framework.test import APIRequestFactory

from common.tests.mixins import MockTestMixin
from tenants.serializers import (
    TenantSerializer,
    OrganizationSerializer
)


class TenantSerializerValidationTestCase(MockTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.serializer = TenantSerializer
        cls.tenant = cls.create_bare_minimum_tenant()

    def test_field_validation_hashes_password(self):
        old_password = self.tenant.password
        data = {
            'email': self.tenant.email,
            'password': 'adifferentpasswordthanthedefaultone'}
        serializer = self.serializer(self.tenant, data=data)

        new_passwd = serializer.validate_password(data['password'])

        self.assertNotEqual(old_password, new_passwd)


class OrganizationSerializerTestCase(MockTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.serializer = OrganizationSerializer
        cls.tenant = cls.create_bare_minimum_tenant()
        cls.factory = APIRequestFactory()

    def test_created_organization_automatically_adds_authenticated_user(self):
        data = {
            'name': 'aaaaaaaaa'
        }
        request = self.factory.post('/some/url')
        request.user = self.tenant.user_ptr
        serializer = self.serializer(data=data, context={'request': request})
        serializer.is_valid()

        organization = serializer.save()

        self.assertIn(self.tenant, organization.users.all())
