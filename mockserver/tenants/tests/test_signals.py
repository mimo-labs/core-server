from django.test import TestCase

from common.tests.mixins import MockTestMixin


class TenantSignalsTestCase(TestCase, MockTestMixin):
    def test_new_tenant_triggers_playground_org_signal(self):
        tenant = self.create_bare_minimum_tenant()

        self.assertEqual(len(tenant.organizations.all()), 1)
        self.assertEqual(tenant.organizations.first().name, 'Playground')
