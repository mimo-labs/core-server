from unittest import mock

from django.test import TestCase

from common.tests.mixins import MockTestMixin
from tenants.models import OrganizationInvite


class OrganizationInviteModelTestCase(MockTestMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        super(OrganizationInviteModelTestCase, cls).setUpClass()
        cls.org = cls.create_bare_minimum_organization()

    @mock.patch('tenants.models.mail_membership_invite.delay')
    def test_invite_task_is_called_on_new_invite(self, patch_invite_task):
        OrganizationInvite.objects.create(
            email='foo@bar.baz',
            from_domain='somedomain',
            organization=self.org,
        )

        patch_invite_task.assert_called_once_with(
            False,
            'foo@bar.baz',
            self.org.name,
            'somedomain',
        )
