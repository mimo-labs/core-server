import uuid

from django.db import models

from authentication.models import User
from base.models import DateAwareModel


class Organization(DateAwareModel):
    name = models.CharField(
        max_length=255
    )
    users = models.ManyToManyField(
        'tenants.Tenant'
    )


class Tenant(DateAwareModel, User):
    tenant_uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )


class OrganizationAwareModel(DateAwareModel):
    organization = models.ForeignKey(
        'tenants.Organization',
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        abstract = True
