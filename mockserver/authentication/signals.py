from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from tenants.models import Tenant


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
@receiver(post_save, sender=Tenant)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(
            user=instance
        )
