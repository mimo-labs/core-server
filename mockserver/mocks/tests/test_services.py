from unittest.mock import patch

from django.test import TestCase

from common.tests.helpers import CaptureValues
from common.tests.mixins import MockTestMixin
from mocks.services import EndpointService
from tenants.models import Project


class EndpointServiceTestCase(MockTestMixin, TestCase):
    service = EndpointService

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.organization = cls.create_bare_minimum_organization()
        cls.project = cls.create_bare_minimum_project(cls.organization)

    def test_get_endpoint_is_idempotent(self):
        endpoint_name = "/foo/bar/baz"

        endpoint = self.service.get_endpoint_by_name_and_project(
            endpoint_name,
            self.project.id
        )
        endpoint2 = self.service.get_endpoint_by_name_and_project(
            endpoint_name,
            self.project.id
        )

        self.assertEqual(endpoint2, endpoint)

    def test_get_endpoint_with_existing_details_returns_existing(self):
        path_name = "/some/path/to/create"
        self.create_bare_minimum_endpoint(self.project, path_name)

        with patch('mocks.services.EndpointService.model.get_or_create',
                   CaptureValues(self.service.model.get_or_create)) as svc_mock:
            self.service.get_endpoint_by_name_and_project(path_name, self.project.id)
            # Return value is a tuple (object, boolean), so we just consider the latter element
            self.assertFalse(svc_mock.return_values[0][1])

    def test_get_endpoint_with_new_details_creates_new_one(self):
        path_name = "/some/path/to/create"

        with patch('mocks.services.EndpointService.model.get_or_create',
                   CaptureValues(self.service.model.get_or_create)) as svc_mock:
            self.service.get_endpoint_by_name_and_project(path_name, self.project.id)
            # Return value is a tuple (object, boolean), so we just consider the latter element
            self.assertTrue(svc_mock.return_values[0][1])

    # Abstraction layers are supposed to deal with nonexistent IDs
    def test_get_endpoint_with_nonexistent_project_id_fails(self):
        last_project_id = Project.objects.last().id

        with self.assertRaises(Project.DoesNotExist):
            self.service.get_endpoint_by_name_and_project("/aaaaaaaa", last_project_id + 1)
