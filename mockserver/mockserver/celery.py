import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mockserver.settings')

app = Celery('mockserver')

app.config_from_object('django.conf:settings')
app.conf.broker_url = os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6379')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
