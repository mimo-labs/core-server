from django.dispatch import receiver
from django.db.models.signals import post_save

from tenants.models import Organization, Tenant


@receiver(post_save, sender=Organization)
def create_organization_tenant(sender, instance=None, created=False, **kwargs):
    if created:
        Tenant.objects.create(
            organization=instance
        )
