import uuid

from django.db import models

from authentication.models import User
from common.models import DateAwareModel


class OrganizationMembership(DateAwareModel):
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE
    )
    organization = models.ForeignKey(
        'tenants.Organization',
        on_delete=models.CASCADE
    )
    is_admin = models.BooleanField(
        default=False
    )

    class Meta:
        unique_together = (
            ('tenant', 'organization'),
        )


class Organization(DateAwareModel):
    name = models.CharField(
        max_length=255
    )
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    is_playground = models.BooleanField(
        default=False
    )
    users = models.ManyToManyField(
        'tenants.Tenant',
        through=OrganizationMembership,
        blank=True
    )


class Tenant(DateAwareModel, User):
    pass


class OrganizationAwareModel(DateAwareModel):
    organization = models.ForeignKey(
        'tenants.Organization',
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        abstract = True
