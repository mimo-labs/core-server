import string
from typing import Optional
from uuid import uuid4
import random

from mocks.models import (
    Mock,
    Endpoint,
    Category,
    HttpVerb,
)
from tenants.models import (
    Organization,
    Tenant,
    OrganizationMembership,
    Project,
)


class MockTestMixin:
    @classmethod
    def create_bare_minimum_category(cls, project: Project) -> Category:
        return Category.objects.create(
            project=project,
            name=''.join(random.choices(string.ascii_lowercase, k=6))
        )

    @classmethod
    def create_bare_minimum_endpoint(
            cls,
            project: Optional[Project] = None,
            path: str = "/foo/bar"
    ) -> Endpoint:
        if not project:
            project = cls.create_bare_minimum_project()
        endpoint = Endpoint.objects.create(
            path=path,
        )
        endpoint.categories.add(cls.create_bare_minimum_category(project))

        return endpoint

    @classmethod
    def create_bare_minimum_verb(cls, organization: Organization) -> HttpVerb:
        verb, _ = HttpVerb.objects.get_or_create(
            name="GET",
            organization=organization
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
    def create_bare_minimum_project(cls, organization: Optional[Organization] = None) -> Project:
        if not organization:
            organization = cls.create_bare_minimum_organization()
        return Project.objects.create(
            name="foobar",
            organization=organization
        )

    @classmethod
    def create_bare_minimum_organization(cls, tenant: Optional[Tenant] = None) -> Organization:
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
                                 None, endpoint: Optional[Endpoint] = None) -> Mock:
        organization = cls.create_bare_minimum_organization(tenant)
        if not project:
            project = cls.create_bare_minimum_project(organization)
        if not endpoint:
            endpoint = cls.create_bare_minimum_endpoint(project)
        return Mock.objects.create(
            title="".join(random.choices(string.ascii_lowercase, k=6)),
            path=endpoint,
            verb=cls.create_bare_minimum_verb(organization),
            status_code=205,
            is_active=True,
        )
