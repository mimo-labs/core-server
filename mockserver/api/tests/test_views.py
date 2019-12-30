from unittest.mock import patch
from uuid import uuid4

from django.http import JsonResponse
from django.test import TestCase, Client

from mocks.models import (
    Header,
    HeaderType
)
from mocks.tests.mixins import MockTestMixin


class MockAPIFetchViewTestCase(TestCase, MockTestMixin):
    def setUp(self):
        self.c = Client()
        self.header_type = HeaderType.objects.create(
            name="Foo"
        )
        self.mock = self.create_bare_minimum_mock()

    @patch('mocks.services.MockService.get_tenant_mocks')
    def test_list_mock_is_allowed(self, patch_get_mock):
        self.mock.content.content = ['foo', 'bar', 'baz']
        self.mock.content.save()
        patch_get_mock.return_value = self.mock

        response: JsonResponse = self.c.get(
            f'{self.mock.path.path}/',
            HTTP_HOST=f'{self.mock.organization.uuid}.localhost'
        )

        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json(), self.mock.content.content)
        self.assertEqual(len(response.json()), 3)

    @patch('mocks.services.MockService.get_tenant_mocks')
    def test_existent_tenant_and_mock_returns_mock_values(self, patch_get_mock):
        patch_get_mock.return_value = self.mock
        header = Header.objects.create(
            header_type=self.header_type,
            value="Bar",
            mock=self.mock
        )

        response: JsonResponse = self.c.get(
            self.mock.path.path,
            HTTP_HOST=f'{self.mock.organization.uuid}.localhost'
        )

        self.assertEqual(response.status_code, self.mock.status_code)
        self.assertEqual(response[header.header_type.name], header.value)

    def test_non_existent_tenant_returns_404(self):
        response = self.c.get(self.mock.path.path, HTTP_HOST=f'{uuid4()}.localhost')

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(response.json(), {'detail': 'organization does not exist'})

    @patch('mocks.services.MockService.get_tenant_mocks')
    def test_non_existent_mock_returns_404(self, patch_get_mock):
        patch_get_mock.return_value = None

        response = self.c.get(
            '/does/not/exist',
            HTTP_HOST=f'{self.mock.organization.uuid}.localhost'
        )

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(response.json(), {'detail': 'mock does not exist'})
