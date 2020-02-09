from django.db import models

from common.models import DateAwareModel


class Technology(DateAwareModel):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Technologies"

    def __str__(self):
        return f"{self.name} ({self.code})"
