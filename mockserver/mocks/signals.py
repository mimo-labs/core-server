from django.db.models.signals import post_delete
from django.dispatch import receiver

from mocks.models import Mock
from mocks.tasks import delete_empty_endpoint


@receiver(post_delete, sender=Mock)
def signal_delete_empty_endpoint(sender, instance: Mock = None, **kwargs):
    if instance.path:
        delete_empty_endpoint.delay(instance.path.path, instance.project.id)
