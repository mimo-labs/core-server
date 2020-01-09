import json
from unittest.mock import Mock
from uuid import uuid4

from django.test import TestCase

from authentication.decorators.tenant_view import tenancy_required


class TenancyRequiredDecoratorTestCase(TestCase):
    def setUp(self):
        self.fn: Mock = Mock()
        self.request = Mock()
        self.decorated_func = tenancy_required(self.fn)

    def test_no_tenant_returns_404_response(self):
        self.request.organization = None

        response = self.decorated_func(self.request)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content), {'detail': 'organization does not exist'})

    def test_existing_tenant_returns_wrapped_function(self):
        self.request.organization = uuid4()

        self.decorated_func(self.request)

        self.fn.assert_called_once()
