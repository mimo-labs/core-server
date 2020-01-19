from django.test import TestCase

from common.tests.mixins import MockTestMixin
from tenants.serializers import TenantSerializer


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

