import uuid

from django.db import models

from authentication.models import User
from common.models import DateAwareModel
from tenants.tasks import mail_membership_invite


class OrganizationAwareModel(DateAwareModel):
    organization = models.ForeignKey(
        'tenants.Organization',
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        abstract = True


class OrganizationMembership(DateAwareModel):
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE
    )
    organization = models.ForeignKey(
        'tenants.Organization',
        on_delete=models.CASCADE
    )
    is_owner = models.BooleanField(
        default=False
    )
    is_admin = models.BooleanField(
        default=False
    )

    class Meta:
        unique_together = (
            ('tenant', 'organization'),
            ('is_owner', 'organization'),
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

    def __str__(self):
        return f"{self.name} ({self.uuid})"


class Tenant(DateAwareModel, User):
    pass


class OrganizationInvite(OrganizationAwareModel):
    email = models.EmailField()
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.SET_NULL,
        null=True
    )
    from_domain = models.CharField(
        max_length=256,
        null=False,
        default="",
    )
    is_accepted = models.BooleanField(
        default=False
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            is_existing = self.tenant is not None
            mail_membership_invite.delay(is_existing, self.email, self.organization.name)
