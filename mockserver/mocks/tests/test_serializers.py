from django.test import TestCase
from rest_framework import serializers

from common.tests.mixins import MockTestMixin
from mocks.serializers import EndpointSerializer, MockSerializer


class EndpointSerializerValidationTestCase(MockTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.serializer = EndpointSerializer
        cls.organization = cls.create_bare_minimum_organization()
        cls.project = cls.create_bare_minimum_project(cls.organization)
        cls.endpoint = cls.create_bare_minimum_endpoint(cls.project)
        cls.category = cls.create_bare_minimum_category(cls.project)

    def test_endpoints_in_same_project_with_different_path_are_valid(self):
        endpoint_data = {
            'path': '/bar/baz',
            'categories': [self.category.id]
        }

        serializer = self.serializer(data=endpoint_data)

        self.assertTrue(serializer.is_valid())

    def test_endpoints_in_same_project_with_same_path_fails_to_create(self):
        endpoint_data = {
            'path': self.endpoint.path,
            'categories': [self.category.id]
        }

        serializer = self.serializer(data=endpoint_data)

        with self.assertRaises(
            serializers.ValidationError,
            msg="An endpoint with the path %s already exists for the project" % self.endpoint.path
        ):
            serializer.is_valid(raise_exception=True)

    def test_endpoints_in_different_project_with_same_oath_are_valid(self):
        other_project = self.create_bare_minimum_project(self.organization)
        other_category = self.create_bare_minimum_category(other_project)
        endpoint_data = {
            'path': self.endpoint.path,
            'categories': [other_category.id],
        }

        serializer = self.serializer(data=endpoint_data)

        self.assertTrue(serializer.is_valid())


class MockSerializerTestCase(MockTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.serializer = MockSerializer
        cls.organization = cls.create_bare_minimum_organization()

    def setUp(self):
        self.mock = self.create_bare_minimum_mock()

    def test_serializer_without_verb_is_represented_as_is(self):
        serializer = self.serializer()
        self.mock.verb = None

        rep = serializer.to_representation(self.mock)

        self.assertIsNone(rep['verb'])

    def test_serializer_with_verb_is_represented_as_object(self):
        serializer = self.serializer()
        self.mock.verb = self.create_bare_minimum_verb(self.organization)

        rep = serializer.to_representation(self.mock)

        self.assertIsInstance(rep['verb'], dict)
