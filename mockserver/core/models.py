from djongo import models
from core import validators


class HeaderType(models.Model):
    name = models.CharField(
        max_length=255,
        primary_key=True
    )

    def __str__(self):
        return self.name


class Mock(models.Model):
    path = models.CharField(
        max_length=255,
        validators=[validators.validate_path],
        primary_key=True
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

    def __str__(self):
        return self.path


class Header(models.Model):
    header_type = models.ForeignKey(
        HeaderType,
        on_delete=models.CASCADE
    )
    value = models.TextField()
    mock = models.ForeignKey(
        Mock,
        on_delete=models.CASCADE
    )

    @property
    def as_response_header(self):
        return self.header_type.name, self.value

    def __str__(self):
        return "%s: %s" % (self.header_type, self.value)
