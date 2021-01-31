from unittest import mock

from django.test import TestCase

from common.tests.mixins import MockTestMixin
from tenants.models import (
    OrganizationInvite,
    OrganizationProfile,
    FeatureFlag
)


class OrganizationModelTestCase(MockTestMixin, TestCase):
    def test_organization_handles_profile(self):
        organization = self.create_bare_minimum_organization()

        with self.subTest("automatically creates profile"):
            self.assertIsNotNone(organization.profile)
            self.assertEqual(OrganizationProfile.objects.count(), 1)
            self.assertEqual(organization.profile.public_name, organization.name)
            self.assertEqual(organization.profile.organization.pk, organization.pk)
        with self.subTest("automatically deletes profile"):
            organization.delete()

            self.assertEqual(OrganizationProfile.objects.count(), 0)


    def test_organization_handles_feature_flags(self):
        organization = self.create_bare_minimum_organization()

        with self.subTest("automatically creates feature flag"):
            self.assertIsNotNone(organization.feature_flags)
            self.assertEqual(FeatureFlag.objects.count(), 1)
        with self.subTest("automatically deletes feature flag"):
            organization.delete()

            self.assertEqual(FeatureFlag.objects.count(), 0)


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
