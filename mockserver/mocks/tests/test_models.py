from django.test import TestCase

from common.tests.mixins import MockTestMixin
from mocks.models import Mock


class MockTestCase(MockTestMixin, TestCase):
    def test_new_empty_mock_is_incomplete(self):
        bare_mock = Mock.objects.create()

        self.assertFalse(bare_mock.is_complete)
        self.assertFalse(bare_mock.is_active)

    def test_new_mock_with_essentials_is_complete(self):
        other_mock = self.create_bare_minimum_mock()

        self.assertTrue(other_mock.is_complete)

    def test_project_property_returns_project_instance(self):
        organization = self.create_bare_minimum_organization()
        project = self.create_bare_minimum_project(organization)
        mock = self.create_bare_minimum_mock(project=project)

        mock_project = mock.project

        self.assertEqual(project, mock_project)

    def test_mock_without_explicit_content_creates_default(self):
        mock = self.create_bare_minimum_mock()

        self.assertEqual(mock.content.get().content, {})

    def test_mock_without_explicit_params_creates_default(self):
        mock = self.create_bare_minimum_mock()

        self.assertEqual(mock.params.get().content, {})

    def test_equal_mocks_deactivates_oldest_one(self):
        mock = self.create_bare_minimum_mock()

        Mock.objects.create(path=mock.path, verb=mock.verb, is_active=True)
        mock.refresh_from_db()

        self.assertFalse(mock.is_active)

    def test_different_mocks_leaves_oldest_active(self):
        endpoint = self.create_bare_minimum_endpoint(path="/bar/baz")
        mock = self.create_bare_minimum_mock()

        self.create_bare_minimum_mock(endpoint=endpoint)
        mock.refresh_from_db()

        self.assertTrue(mock.is_active)

    def test_equal_mocks_with_new_inactive_leaves_oldest_active(self):
        mock = self.create_bare_minimum_mock()

        Mock.objects.create(path=mock.path, verb=mock.verb, is_active=False)
        mock.refresh_from_db()

        self.assertTrue(mock.is_active)
