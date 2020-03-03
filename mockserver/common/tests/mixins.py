import string
from typing import Optional
from uuid import uuid4
import random

from mocks.models import (
    Mock,
    Endpoint,
    HttpVerb
)
from tenants.models import (
    Organization,
    Tenant,
    OrganizationMembership
)


class MockTestMixin:
    @classmethod
    def create_bare_minimum_path(cls):
        return Endpoint.objects.create(
            path="/foo/bar"
        )

    @classmethod
    def create_bare_minimum_verb(cls):
        return HttpVerb.objects.create(
            name="GET"
        )

    @classmethod
    def create_bare_minimum_tenant(cls) -> Tenant:
        random_email = ''.join(random.choices(string.ascii_lowercase, k=6))
        tenant = Tenant.objects.create(
            email=f'{random_email}@localhost',
        )
        tenant.set_password('passwd')
        tenant.save()
        return tenant

    @classmethod
    def create_bare_minimum_organization(cls, tenant: Optional[Tenant] = None):
        org = Organization.objects.create(
            name="foobar",
            uuid=uuid4()
        )
        if tenant:
            OrganizationMembership.objects.create(
                organization=org,
                tenant=tenant
            )

        return org

    @classmethod
    def create_bare_minimum_mock(cls, tenant: Optional[Tenant] = None):
        return Mock.objects.create(
            title="foobar",
            path=cls.create_bare_minimum_path(),
            verb=cls.create_bare_minimum_verb(),
            status_code=205,
            organization=cls.create_bare_minimum_organization(tenant),
        )
