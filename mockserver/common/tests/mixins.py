import string
from typing import Optional
from uuid import uuid4
import random

from mocks.models import (
    Mock,
    Endpoint,
    HttpVerb,
    Project
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
        verb, _ = HttpVerb.objects.get_or_create(
            name="GET"
        )
        return verb

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
    def create_bare_minimum_project(cls, organization: Optional[Organization] = None):
        return Project.objects.create(
            name="foobar",
            organization=organization
        )

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
        organization = cls.create_bare_minimum_organization(tenant)
        return Mock.objects.create(
            title="".join(random.choices(string.ascii_lowercase, k=6)),
            path=cls.create_bare_minimum_path(),
            verb=cls.create_bare_minimum_verb(),
            status_code=205,
            project=cls.create_bare_minimum_project(organization),
        )
