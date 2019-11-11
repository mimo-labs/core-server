import uuid

from django.conf import settings
from django.db import models

from base.models import DateAwareModel


class Organization(DateAwareModel):
    name = models.CharField(
        max_length=255
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL
    )


class Tenant(DateAwareModel):
    tenant_uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE
    )


class TenantAwareModel(DateAwareModel):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True
