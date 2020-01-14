from unittest.mock import (
    Mock,
    PropertyMock,
    patch
)

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from authentication.serializers import PasswordResetSerializer
from common.tests.mixins import MockTestMixin


class PasswordResetSerializerTestCase(TestCase, MockTestMixin):
    @classmethod
    def setUpClass(cls):
        super(PasswordResetSerializerTestCase, cls).setUpClass()
        cls.tenant = cls.create_bare_minimum_tenant()
        cls.serializer = PasswordResetSerializer
        cls.mock_context = Mock()
        cls.mock_context.user = cls.tenant
        cls.context = {'request': cls.mock_context}

    def test_serializer_with_anonymous_user_raises_error(self):
        with patch('tenants.models.Tenant.is_anonymous', new_callable=PropertyMock) as mock_anon:
            mock_anon.return_value = True
            serializer = self.serializer(data={'new_password': 'asd123'}, context=self.context)

            with self.assertRaises(ValidationError, msg='a user is required'):
                serializer.is_valid(raise_exception=True)

    def test_serializer_with_existing_user_changes_password(self):
        new_password = 'foobarbaz'
        serializer = self.serializer(data={'new_password': new_password}, context=self.context)
        serializer.is_valid(raise_exception=True)

        ret = serializer.save()

        self.assertTrue(ret.check_password(new_password))
