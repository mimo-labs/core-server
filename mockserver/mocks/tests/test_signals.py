from unittest.mock import patch

from django.test import TransactionTestCase

from common.tests.mixins import MockTestMixin
from mocks.signals import signal_delete_empty_endpoint


class EndpointSignalsTestCase(MockTestMixin, TransactionTestCase):
    def setUp(self):
        super().setUp()
        self.patcher = patch('mocks.signals.delete_empty_endpoint.delay')
        self.mock_task = self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.mock = self.create_bare_minimum_mock()

    def test_delete_mock_without_path_does_nothing(self):
        self.mock.path = None

        signal_delete_empty_endpoint(None, self.mock)

        self.assertFalse(self.mock_task.called)

    def test_delete_mock_with_path_triggers_async_task(self):
        signal_delete_empty_endpoint(None, self.mock)

        self.assertTrue(self.mock_task.called)
