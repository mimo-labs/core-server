from unittest.mock import (
    Mock,
    patch
)
from uuid import uuid4

from django.contrib.auth.models import AnonymousUser
from django.test import (
    TestCase,
    RequestFactory
)

from tenants.middlewares.tenant import TenantMiddleware


class TenantMiddlewareTestCase(TestCase):
    def setUp(self):
        self.response_mock = Mock()
        self.middleware = TenantMiddleware(self.response_mock)

    @patch('tenants.middlewares.tenant.organization_from_request')
    def test_middleware_call_always_adds_organization_attribute(self, patch_tenant_service):
        patch_tenant_service.return_value = uuid4()
        request = RequestFactory().get('/')
        request.user = AnonymousUser()

        self.middleware(request)

        assert hasattr(request, 'organization')
