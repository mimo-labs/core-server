from django.db.models.signals import post_save
from django.dispatch import receiver

from tenants.models import (
    Tenant,
    Organization,
    OrganizationMembership
)
from tenants.services import OrganizationService


@receiver(post_save, sender=Tenant)
def create_playground_organization(sender, instance=None, created=False, **kwargs):
    if created:
        org = Organization.objects.create(
            name='Playground',
            is_playground=True
        )
        OrganizationMembership.objects.create(
            tenant=instance,
            organization=org,
            is_owner=True,
            is_admin=True
        )


@receiver(post_save, sender=Organization)
def bootstrap_organization(sender, instance=None, created=False, **kwargs):
    if created:
        OrganizationService.bootstrap_organization(organization=instance)
