from django.test import TestCase
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIRequestFactory

from authentication.backends import MailingTokenAuthentication
from authentication.models import OneOffToken
from common.tests.mixins import MockTestMixin


factory = APIRequestFactory()


class MailingTokenAuthenticationTestCase(MockTestMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        super(MailingTokenAuthenticationTestCase, cls).setUpClass()
        cls.tenant = cls.create_bare_minimum_tenant()
        cls.authentication = MailingTokenAuthentication()

    def test_token_is_deleted_after_use(self):
        token = OneOffToken.objects.create(
            user=self.tenant
        )
        request = factory.post(
            '/someurl',
            HTTP_AUTHORIZATION=f'MailToken {token.key}'
        )

        first_authentication = self.authentication.authenticate(request)

        self.assertEqual(first_authentication[0].email, self.tenant.email)
        self.assertIsNone(first_authentication[1])
        with self.assertRaises(AuthenticationFailed, msg='Invalid token.'):
            self.authentication.authenticate(request)
