from djongo import models
from core import validators

# Create your models here.


class Mock(models.Model):
    path = models.CharField(
        max_length=255,
        validators=[validators.validate_path]
    )
    verb = models.CharField(
        max_length=20,
        default='GET'
    )
    content = models.TextField(
        validators=[validators.validate_json]
    )
    status_code = models.IntegerField(
        default=200
    )
