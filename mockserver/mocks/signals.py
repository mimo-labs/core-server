from django.db.models.signals import post_save
from django.dispatch import receiver

from mocks.models import (
    Mock,
    Content,
    Params
)


@receiver(post_save, sender=Mock)
def create_mock_contents(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, 'content'):
            instance.content = Content.objects.create(
                mock=instance
            )
        if not hasattr(instance, 'params'):
            instance.params = Params.objects.create(
                mock=instance
            )
        instance.save()
