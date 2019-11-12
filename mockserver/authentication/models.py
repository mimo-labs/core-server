from django.db import models

from base.models import DateAwareModel
from tenants.models import Tenant


class TenantAwareModel(DateAwareModel):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True
