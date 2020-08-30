from unittest.mock import patch

from django.test import TestCase

from common.tests.mixins import MockTestMixin
from mocks.tasks import delete_empty_endpoint


class EndpointCleanupTaskTestCase(MockTestMixin, TestCase):
    task = delete_empty_endpoint

    def setUp(self):
        super().setUp()
        self.patcher = patch('mocks.tasks.EndpointService.cleanup_endpoint')
        self.mock_service = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.create_bare_minimum_project()
        cls.endpoint = cls.create_bare_minimum_endpoint(project=cls.project)

    def test_run_with_unique_mock_calls_service_method(self):
        self.task(self.endpoint.path, self.project.id)

        self.assertTrue(self.mock_service)

    def test_run_with_multiple_mocks_calls_service_method(self):
        self.create_bare_minimum_mock(project=self.project, endpoint=self.endpoint)
        self.task(self.endpoint.path, self.project.id)

        self.assertTrue(self.mock_service)
