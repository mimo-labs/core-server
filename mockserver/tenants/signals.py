from django.db.models.signals import post_save
from django.dispatch import receiver

from tenants.models import (
    Tenant,
    Organization
)


@receiver(post_save, sender=Tenant)
def create_playground_organization(sender, instance=None, created=False, **kwargs):
    if created:
        org = Organization.objects.create(
            name='Playground',
            is_playground=True
        )
        org.users.add(instance)
