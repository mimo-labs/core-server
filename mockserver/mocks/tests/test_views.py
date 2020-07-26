from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

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
        self.client.defaults["SERVER_NAME"] = "%s.%s.localhost" % (
            self.organization.uuid,
            self.project.name
        )
        self.mock = self.create_bare_minimum_mock(self.tenant, self.project)

    def test_unauthenticated_detail_request_is_disallowed(self):
        url = reverse('v1:mock-detail', kwargs={'pk': self.mock.id})

        response = self.client.get(url)

        self.assertEqual(401, response.status_code)

    def test_unauthenticated_list_request_is_disallowed(self):
        url = reverse('v1:mock-list')

        response = self.client.get(url)

        self.assertEqual(401, response.status_code)

    def test_user_not_in_mock_organization_is_disallowed(self):
        other_tenant = self.create_bare_minimum_tenant()
        token = other_tenant.user_ptr.auth_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        url = reverse('v1:mock-detail', kwargs={'pk': self.mock.id})

        response = self.client.get(url)

        self.assertEqual(403, response.status_code)

    def test_user_in_mock_organization_is_allowed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        url = reverse('v1:mock-detail', kwargs={'pk': self.mock.id})

        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

    def test_list_without_project_id_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        url = reverse('v1:mock-list')

        response = self.client.get(url)

        self.assertEqual(400, response.status_code)
        self.assertEqual('project_id is required', response.json()['detail'])

    def test_list_with_unauthorized_project_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        url = reverse('v1:mock-list')
        other_organization = self.create_bare_minimum_organization()
        other_project = self.create_bare_minimum_project(other_organization)

        response = self.client.get(url, {'project_id': other_project.id})

        self.assertEqual(403, response.status_code)

    def test_list_with_nonexistent_project_returns_404(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        url = reverse('v1:mock-list')

        response = self.client.get(url, {'project_id': self.project.id + 1})

        self.assertEqual(404, response.status_code)

    def test_with_user_project_returns_filtered(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        url = reverse('v1:mock-list')
        other_organization = self.create_bare_minimum_organization()
        other_project = self.create_bare_minimum_project(other_organization)
        # create a mock on a different project
        self.create_bare_minimum_mock(self.tenant, other_project)

        response = self.client.get(url, {'project_id': self.project.id})

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json()))


class CategoryViewSetTestCase(APITestCase, MockTestMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tenant = cls.create_bare_minimum_tenant()
        cls.organization = cls.create_bare_minimum_organization(cls.tenant)
        cls.project = cls.create_bare_minimum_project(cls.organization)
        cls.token = Token.objects.get(user=cls.tenant)

    def setUp(self):
        self.client.defaults["SERVER_NAME"] = "%s.%s.localhost" % (
            self.organization.uuid,
            self.project.name
        )

    def test_list_without_project_id_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        url = reverse('v1:category-list')

        response = self.client.get(url)

        self.assertEqual(400, response.status_code)
        self.assertEqual('project_id is required', response.json()['detail'])

    def test_list_with_unauthorized_project_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        url = reverse('v1:category-list')
        other_organization = self.create_bare_minimum_organization()
        other_project = self.create_bare_minimum_project(other_organization)

        response = self.client.get(url, {'project_id': other_project.id})

        self.assertEqual(403, response.status_code)

    def test_list_with_nonexistent_project_returns_404(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        url = reverse('v1:category-list')

        response = self.client.get(url, {'project_id': self.project.id + 1})

        self.assertEqual(404, response.status_code)

    def test_with_user_project_returns_filtered(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        url = reverse('v1:category-list')
        other_organization = self.create_bare_minimum_organization()
        other_project = self.create_bare_minimum_project(other_organization)
        # create a category on a different project
        self.create_bare_minimum_category(self.project)
        self.create_bare_minimum_category(other_project)

        response = self.client.get(url, {'project_id': self.project.id})

        self.assertEqual(200, response.status_code)
        # 2 categories: default for project, and a custom created one
        self.assertEqual(2, len(response.json()))


class EndpointViewSetTestCase(APITestCase, MockTestMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tenant = cls.create_bare_minimum_tenant()
        cls.organization = cls.create_bare_minimum_organization(cls.tenant)
        cls.project = cls.create_bare_minimum_project(cls.organization)
        cls.token = Token.objects.get(user=cls.tenant)

    def setUp(self):
        self.client.defaults["SERVER_NAME"] = "%s.%s.localhost" % (
            self.organization.uuid,
            self.project.name
        )

    def test_list_without_project_id_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        url = reverse('v1:endpoint-list')

        response = self.client.get(url)

        self.assertEqual(400, response.status_code)
        self.assertEqual('project_id is required', response.json()['detail'])

    def test_list_with_unauthorized_project_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        url = reverse('v1:endpoint-list')
        other_organization = self.create_bare_minimum_organization()
        other_project = self.create_bare_minimum_project(other_organization)

        response = self.client.get(url, {'project_id': other_project.id})

        self.assertEqual(403, response.status_code)

    def test_list_with_nonexistent_project_returns_404(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        url = reverse('v1:endpoint-list')

        response = self.client.get(url, {'project_id': self.project.id + 1})

        self.assertEqual(404, response.status_code)

    def test_with_user_project_returns_filtered(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        url = reverse('v1:endpoint-list')
        other_organization = self.create_bare_minimum_organization()
        other_project = self.create_bare_minimum_project(other_organization)
        # create an endpoint on a different project
        self.create_bare_minimum_endpoint(self.project)
        self.create_bare_minimum_endpoint(other_project)

        response = self.client.get(url, {'project_id': self.project.id})

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json()))
