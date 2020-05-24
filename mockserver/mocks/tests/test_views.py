from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from common.tests.mixins import MockTestMixin


class MockViewSetTestCase(APITestCase, MockTestMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tenant = cls.create_bare_minimum_tenant()
        cls.organization = cls.create_bare_minimum_organization(cls.tenant)
        cls.project = cls.create_bare_minimum_project(cls.organization)
        cls.token = Token.objects.get(user=cls.tenant)

    def setUp(self):
        self.c = APIClient()
        self.c.defaults["SERVER_NAME"] = "%s.%s.localhost" % (
            self.organization.uuid,
            self.project.name
        )
        self.mock = self.create_bare_minimum_mock(self.tenant, self.project)

    def test_unauthenticated_detail_request_is_disallowed(self):
        url = reverse('v1:mock-detail', kwargs={'pk': self.mock.id})

        response = self.c.get(url)

        self.assertEqual(401, response.status_code)

    def test_unauthenticated_list_request_is_disallowed(self):
        url = reverse('v1:mock-list')

        response = self.c.get(url)

        self.assertEqual(401, response.status_code)

    def test_user_not_in_mock_organization_is_disallowed(self):
        other_tenant = self.create_bare_minimum_tenant()
        token = other_tenant.user_ptr.auth_token
        self.c.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        url = reverse('v1:mock-detail', kwargs={'pk': self.mock.id})

        response = self.c.get(url)

        self.assertEqual(403, response.status_code)

    def test_user_in_mock_organization_is_allowed(self):
        self.c.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        url = reverse('v1:mock-detail', kwargs={'pk': self.mock.id})

        response = self.c.get(url)

        self.assertEqual(200, response.status_code)
