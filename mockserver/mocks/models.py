from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.postgres.fields import JSONField

from authentication.models import TenantAwareModel
from base.models import DateAwareModel
from base.validators import validate_path


class Category(DateAwareModel):
    name = models.CharField(
        max_length=255
    )

    class Meta:
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Endpoint(DateAwareModel):
    path = models.CharField(
        max_length=2048,
        validators=(validate_path,),
        default='/'
    )
    category = models.ForeignKey(
        'mocks.Category',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.path


class Content(DateAwareModel):
    mock = models.ForeignKey(
        'mocks.Mock',
        on_delete=models.CASCADE
    )
    content = JSONField(
        default=dict
    )


class Params(DateAwareModel):
    mock = models.ForeignKey(
        'mocks.Mock',
        on_delete=models.CASCADE
    )
    content = JSONField(
        default=dict
    )


class Mock(TenantAwareModel):
    title = models.CharField(
        max_length=255,
        primary_key=True
    )
    path = models.ForeignKey(
        'mocks.Endpoint',
        on_delete=models.PROTECT
    )
    verb = models.ForeignKey(
        'mocks.HttpVerb',
        on_delete=models.PROTECT
    )
    status_code = models.IntegerField(
        default=200
    )
    is_active = models.BooleanField(
        default=True
    )

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


class HeaderType(DateAwareModel):
    name = models.CharField(
        max_length=255,
        primary_key=True
    )

    def __str__(self):
        return self.name


class HttpVerb(DateAwareModel):
    name = models.CharField(
        max_length=255,
        primary_key=True
    )

    class Meta:
        verbose_name = _('HTTP Verb')
        verbose_name_plural = _('HTTP Verbs')

    def __str__(self):
        return self.name


class Header(DateAwareModel):
    header_type = models.ForeignKey(
        'mocks.HeaderType',
        on_delete=models.CASCADE
    )
    value = models.TextField()
    mock = models.ForeignKey(
        'mocks.Mock',
        on_delete=models.CASCADE
    )

    @property
    def as_response_header(self):
        return self.header_type.name, self.value

    def __str__(self):
        return "%s: %s" % (self.header_type, self.value)
