from uuid import uuid4

from mocks.models import (
    Mock,
    Endpoint,
    HttpVerb
)
from tenants.models import Organization


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
    def create_bare_minimum_organization(cls):
        return Organization.objects.create(
            name="foobar",
            uuid=uuid4()
        )

    @classmethod
    def create_bare_minimum_mock(cls):
        return Mock.objects.create(
            title="foobar",
            path=cls.create_bare_minimum_path(),
            verb=cls.create_bare_minimum_verb(),
            status_code=205,
            organization=cls.create_bare_minimum_organization(),
        )
