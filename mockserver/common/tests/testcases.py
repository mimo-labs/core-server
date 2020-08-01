from rest_framework.test import APITestCase

from common.tests.mixins import MockTestMixin


class APIViewSetTestCase(APITestCase, MockTestMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.tenant = cls.create_bare_minimum_tenant()
        cls.organization = cls.create_bare_minimum_organization(cls.tenant)
        cls.project = cls.create_bare_minimum_project(cls.organization)
        cls.mock = cls.create_bare_minimum_mock(cls.tenant, cls.project)

    def setUp(self):
        self.client.defaults["SERVER_NAME"] = "%s.%s.localhost" % (
            self.organization.uuid,
            self.project.name
        )
        self.tenant.refresh_from_db()
        self.organization.refresh_from_db()
        self.project.refresh_from_db()
        self.mock.refresh_from_db()
