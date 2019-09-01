from djongo import models
from core import validators


class HeaderType(models.Model):
    name = models.CharField(
        max_length=255,
        primary_key=True
    )

    def __str__(self):
        return self.name


class HttpVerb(models.Model):
    name = models.CharField(
        max_length=255,
        primary_key=True
    )

    def __str__(self):
        return self.name


class Mock(models.Model):
    title = models.CharField(
        max_length=255,
        primary_key=True
    )
    path = models.CharField(
        max_length=955,
        validators=[validators.validate_path]
    )
    params = models.TextField(
        validators=[validators.validate_json],
        null=True,
        blank=True
    )
    verb = models.ForeignKey(
        HttpVerb,
        on_delete=models.PROTECT
    )
    content = models.TextField(
        validators=[validators.validate_json]
    )
    status_code = models.IntegerField(
        default=200
    )

    def __str__(self):
        return self.title


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
