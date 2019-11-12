import uuid

from django.db import models
from django.conf import settings

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
