import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from mocks.models import (
    Mock,
    Content,
    Params
)


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Mock)
def create_mock_contents(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, 'content'):
            logger.info(f'create default content mock {instance.pk} \
                          tenant {instance.organization.uuid}')
            instance.content = Content.objects.create(
                mock=instance
            )
        if not hasattr(instance, 'params'):
            logger.info(f'create default params mock {instance.pk} \
                          tenant {instance.organization.uuid}')
            instance.params = Params.objects.create(
                mock=instance
            )
        instance.save()
