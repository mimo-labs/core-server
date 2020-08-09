from django.urls import reverse
from rest_framework.authtoken.models import Token

from common.tests.testcases import APIViewSetTestCase
from tenants.models import Project, Organization


class MockViewSetTestCase(APIViewSetTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.token = Token.objects.get(user=cls.tenant)

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
        last_project_id = Project.objects.last().id

        response = self.client.get(url, {'project_id': last_project_id + 1})

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


class CategoryViewSetTestCase(APIViewSetTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.token = Token.objects.get(user=cls.tenant)

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
        last_project_id = Project.objects.last().id

        response = self.client.get(url, {'project_id': last_project_id + 1})

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
        # 3 categories: default for project, default for mock, and a custom created one
        self.assertEqual(3, len(response.json()))


class EndpointViewSetTestCase(APIViewSetTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.token = Token.objects.get(user=cls.tenant)

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
        last_project_id = Project.objects.last().id

        response = self.client.get(url, {'project_id': last_project_id + 1})

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
        # 2 endpoints: one created now, one for the base case mock
        self.assertEqual(2, len(response.json()))


class HttpVerbViewSetTestCase(APIViewSetTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.token = Token.objects.get(user=cls.tenant)
        cls.url = reverse('v1:httpverb-list')

    def test_list_without_organization_is_denied(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        response = self.client.get(self.url)

        self.assertEqual(400, response.status_code)
        self.assertEqual('organization_id is required', response.json()['detail'])

    def test_list_with_nonexistent_organization_returns_404(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        last_organization_id = Organization.objects.last().id

        response = self.client.get(self.url, {'organization_id': last_organization_id + 1})

        self.assertEqual(404, response.status_code)
        self.assertEqual('organization does not exist', response.json()['detail'])

    def test_list_with_unauthorized_organization_is_denied(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        other_organization = self.create_bare_minimum_organization()

        response = self.client.get(self.url, {'organization_id': other_organization.id})

        self.assertEqual(403, response.status_code)

    def test_list_with_authorized_organization_returns_scoped(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        # This creates 5 more verbs
        self.create_bare_minimum_organization()

        response = self.client.get(self.url, {'organization_id': self.organization.id})

        self.assertEqual(200, response.status_code)
        self.assertEqual(5, len(response.json()))


class HeaderTypeViewSetTestCase(APIViewSetTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.token = Token.objects.get(user=cls.tenant)
        cls.url = reverse('v1:headertype-list')

    def test_list_without_organization_is_denied(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        response = self.client.get(self.url)

        self.assertEqual(400, response.status_code)
        self.assertEqual('organization_id is required', response.json()['detail'])

    def test_list_with_nonexistent_organization_returns_404(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        last_organization_id = Organization.objects.last().id

        response = self.client.get(self.url, {'organization_id': last_organization_id + 1})

        self.assertEqual(404, response.status_code)
        self.assertEqual('organization does not exist', response.json()['detail'])

    def test_list_with_unauthorized_organization_is_denied(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        other_organization = self.create_bare_minimum_organization()

        response = self.client.get(self.url, {'organization_id': other_organization.id})

        self.assertEqual(403, response.status_code)

    def test_list_with_authorized_organization_returns_scoped(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        # This creates 4 more headers
        self.create_bare_minimum_organization()

        response = self.client.get(self.url, {'organization_id': self.organization.id})

        self.assertEqual(200, response.status_code)
        self.assertEqual(4, len(response.json()))
