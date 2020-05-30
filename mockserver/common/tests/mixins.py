import string
from typing import Optional
from uuid import uuid4
import random

from mocks.models import (
    Mock,
    Endpoint,
    HttpVerb,
    Project,
    Category,
)
from tenants.models import (
    Organization,
    Tenant,
    OrganizationMembership
)


class MockTestMixin:
    @classmethod
    def create_bare_minimum_category(cls, project: Project):
        return Category.objects.create(
            project=project,
            name=''.join(random.choices(string.ascii_lowercase, k=6))
        )

    @classmethod
    def create_bare_minimum_endpoint(cls, project: Optional[Project] = None):
        if not project:
            project = cls.create_bare_minimum_project()
        return Endpoint.objects.create(
            path="/foo/bar",
            category=cls.create_bare_minimum_category(project)
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
    def create_bare_minimum_mock(cls, tenant: Optional[Tenant] = None, project: Optional[Project] =
                                None):
        organization = cls.create_bare_minimum_organization(tenant)
        if not project:
            project = cls.create_bare_minimum_project(organization)
        return Mock.objects.create(
            title="".join(random.choices(string.ascii_lowercase, k=6)),
            path=cls.create_bare_minimum_endpoint(project),
            verb=cls.create_bare_minimum_verb(),
            status_code=205,
        )
