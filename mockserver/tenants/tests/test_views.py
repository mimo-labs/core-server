from unittest.mock import (
    patch,
    MagicMock,
    Mock
)

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from common.tests.mixins import MockTestMixin


class OrganizationViewSetTestCase(MockTestMixin, APITestCase):
    def setUp(self):
        self.tenant = self.create_bare_minimum_tenant()
        self.organization = self.create_bare_minimum_organization()
        self.project = self.create_bare_minimum_project(self.organization)
        self.client.defaults['SERVER_NAME'] = "%s.%s.localhost" % (
            self.organization.uuid,
            self.project.name
        )

    def test_unauthenticated_requests_are_disallowed(self):
        with self.subTest('list should be disallowed'):
            url = reverse('v1:organization-list')
            response = self.client.get(url)

            self.assertEqual(response.status_code, 401)

        with self.subTest('detail should be disallowed'):
            url = reverse('v1:organization-detail', kwargs={'pk': self.organization.pk})
            response = self.client.get(url)

            self.assertEqual(response.status_code, 401)

        with self.subTest('member invite should be disallowed'):
            url = reverse('v1:organization-member-invite', kwargs={'pk': self.organization.pk})
            response = self.client.post(url)

            self.assertEqual(response.status_code, 401)

        with self.subTest('profile should be disallowed'):
            url = reverse('v1:organization-profile', kwargs={'pk': self.organization.pk})
            response = self.client.put(url)

            self.assertEqual(response.status_code, 401)

        with self.subTest('promotion should be disallowed'):
            url = reverse('v1:organization-member-promotion', kwargs={'pk': self.organization.pk})
            response = self.client.post(url)

            self.assertEqual(response.status_code, 401)

        with self.subTest('demotion should be disallowed'):
            url = reverse('v1:organization-member-demotion', kwargs={'pk': self.organization.pk})
            response = self.client.post(url)

            self.assertEqual(response.status_code, 401)

    def test_authenticated_non_organization_member_requests_are_disallowed(self):
        url = reverse('v1:organization-detail', kwargs={'pk': self.organization.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tenant.user_ptr.auth_token}')
        with self.subTest('retrieve should be disallowed'):
            response = self.client.get(url)

            self.assertEqual(response.status_code, 403)

        with self.subTest('update should be disallowed'):
            response = self.client.put(url)

            self.assertEqual(response.status_code, 403)

        with self.subTest('delete should be disallowed'):
            response = self.client.delete(url)

            self.assertEqual(response.status_code, 403)

        with self.subTest('member invite should be disallowed'):
            url = reverse('v1:organization-member-invite', kwargs={'pk': self.organization.pk})
            response = self.client.post(url)

            self.assertEqual(response.status_code, 403)

        with self.subTest('organization profile should be disallowed'):
            url = reverse('v1:organization-profile', kwargs={'pk': self.organization.pk})
            response = self.client.put(url)

            self.assertEqual(response.status_code, 403)

        with self.subTest('member promotion should be disallowed'):
            url = reverse('v1:organization-member-promotion', kwargs={'pk': self.organization.pk})
            response = self.client.post(url)

            self.assertEqual(response.status_code, 403)

        with self.subTest('member demotion should be disallowed'):
            url = reverse('v1:organization-member-demotion', kwargs={'pk': self.organization.pk})
            response = self.client.post(url)

            self.assertEqual(response.status_code, 403)

    @patch('tenants.views.Organization.objects', new=MagicMock())
    def test_authenticated_list_requests_are_allowed(self):
        url = reverse('v1:organization-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tenant.user_ptr.auth_token}')
        with self.subTest('list should be allowed'):
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)

        with self.subTest('create should be allowed'):
            response = self.client.post(url)

            self.assertEqual(response.status_code, 400)  # invalid but allowed creation request

    @patch('tenants.views.Organization.objects', new=MagicMock())
    def test_authenticated_member_detail_is_allowed(self):
        url = reverse('v1:organization-detail', kwargs={'pk': self.organization.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tenant.user_ptr.auth_token}')
        self.organization.organizationmembership_set.create(
            organization=self.organization,
            tenant=self.tenant
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_authenticated_admin_update_is_allowed(self):
        url = reverse('v1:organization-detail', kwargs={'pk': self.organization.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tenant.user_ptr.auth_token}')
        self.organization.organizationmembership_set.create(
            organization=self.organization,
            tenant=self.tenant,
            is_admin=True
        )

        response = self.client.put(url)

        self.assertEqual(response.status_code, 400)  # invalid but allowed update request

    def test_authenticated_owner_delete_is_allowed(self):
        url = reverse('v1:organization-detail', kwargs={'pk': self.organization.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tenant.user_ptr.auth_token}')
        self.organization.organizationmembership_set.create(
            organization=self.organization,
            tenant=self.tenant,
            is_owner=True
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)

    @patch('tenants.views.OrganizationViewSet.get_serializer', new=Mock())
    def test_authenticated_owner_promotion_is_allowed(self):
        url = reverse('v1:organization-member-promotion', kwargs={'pk': self.organization.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tenant.user_ptr.auth_token}')
        self.organization.organizationmembership_set.create(
            organization=self.organization,
            tenant=self.tenant,
            is_owner=True
        )

        response = self.client.post(url)

        self.assertEqual(response.status_code, 204)

    @patch('tenants.views.OrganizationViewSet.get_serializer', new=Mock())
    def test_authenticated_owner_demotion_is_allowed(self):
        url = reverse('v1:organization-member-demotion', kwargs={'pk': self.organization.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tenant.user_ptr.auth_token}')
        self.organization.organizationmembership_set.create(
            organization=self.organization,
            tenant=self.tenant,
            is_owner=True
        )

        response = self.client.post(url)

        self.assertEqual(response.status_code, 204)

    @patch('tenants.views.OrganizationViewSet.get_serializer')
    def test_empty_body_calls_no_invites(self, patch_serializer):
        body = {
            'emails': []
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tenant.user_ptr.auth_token}')
        self.organization.organizationmembership_set.create(
            organization=self.organization,
            tenant=self.tenant,
            is_owner=True
        )
        url = reverse('v1:organization-member-invite', kwargs={'pk': self.organization.pk})

        response = self.client.post(url, body, format='json')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b'')
        self.assertFalse(patch_serializer.called)

    @patch('tenants.views.OrganizationViewSet.get_serializer')
    def test_n_emails_call_n_invites(self, patch_serializer):
        emails = ['foo@bar.baz', 'bar@baz.quux', 'yet@another.mail']
        body = {
            'emails': emails
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tenant.user_ptr.auth_token}')
        self.organization.organizationmembership_set.create(
            organization=self.organization,
            tenant=self.tenant,
            is_owner=True
        )
        url = reverse('v1:organization-member-invite', kwargs={'pk': self.organization.pk})

        response = self.client.post(url, body, format='json')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b'')
        self.assertEqual(patch_serializer.call_count, len(emails))

    @patch('tenants.views.OrganizationViewSet.get_serializer')
    def test_authenticated_owner_profile_update_is_allowed(self, patch_serializer):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tenant.user_ptr.auth_token}')
        self.organization.organizationmembership_set.create(
            organization=self.organization,
            tenant=self.tenant,
            is_owner=True
        )
        mock_serializer = Mock()
        mock_serializer.data = {}
        patch_serializer.return_value = mock_serializer
        url = reverse('v1:organization-profile', kwargs={'pk': self.organization.pk})

        response = self.client.put(url)

        self.assertEqual(response.status_code, 200)
