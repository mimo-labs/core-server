from django.db import models

from common.models import DateAwareModel


class Technology(DateAwareModel):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=255)
