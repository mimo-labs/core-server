from django.utils.translation import gettext_lazy as _
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

    class Meta:
        verbose_name = _('HTTP Verb')
        verbose_name_plural = _('HTTP Verbs')

    def __str__(self):
        return self.name


class Mock(models.Model):
    title = models.CharField(
        max_length=255,
        primary_key=True
    )
    path = models.CharField(
        max_length=955,
        validators=[validators.validate_path],
        default='/'
    )
    params = models.TextField(
        validators=[validators.validate_json],
        default='{}'
    )
    verb = models.ForeignKey(
        HttpVerb,
        on_delete=models.PROTECT
    )
    content = models.TextField(
        validators=[validators.validate_json],
        default='{}'
    )
    status_code = models.IntegerField(default=200)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        active_mocks = Mock.objects.filter(
            path=self.path,
            is_active=True
        )

        if active_mocks.exists():
            active_mocks.update(is_active=False)

        return super().save(*args, **kwargs)

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
