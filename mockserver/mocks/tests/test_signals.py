from unittest.mock import (
    Mock,
    patch
)

from django.test import TestCase

from mocks import signals


class MockContentSignalTestCase(TestCase):
    def setUp(self):
        self.created = True
        self.mock = Mock()

    @patch('mocks.models.Content.objects.create')
    @patch('mocks.models.Params.objects.create')
    def test_created_mock_creates_empty_content_and_params(self, patch_params_create,
                                                           patch_content_create):
        patch_params_create.return_value = Mock()
        patch_content_create.return_value = Mock()
        delattr(self.mock, "content")
        delattr(self.mock, "params")

        signals.create_mock_contents('test', self.mock, self.created)

        patch_params_create.assert_called_once()
        patch_content_create.assert_called_once()

    @patch('mocks.models.Content.objects.create')
    @patch('mocks.models.Params.objects.create')
    def test_edited_mock_does_nothing(self, patch_params_create, patch_content_create):
        self.created = False

        signals.create_mock_contents('test', self.mock, self.created)

        assert not patch_params_create.called
        assert not patch_content_create.called

    @patch('mocks.models.Content.objects.create')
    @patch('mocks.models.Params.objects.create')
    def test_created_mock_with_content_and_params_does_nothing(self, patch_params_create,
                                                               patch_content_create):
        self.mock.content = Mock()
        self.mock.params = Mock()

        signals.create_mock_contents('test', self.mock, self.created)

        assert not patch_params_create.called
        assert not patch_content_create.called
