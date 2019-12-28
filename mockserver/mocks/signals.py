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
        instance.content = Content.objects.create(
            mock=instance
        )
        instance.params = Params.objects.create(
            mock=instance
        )
        instance.save()
