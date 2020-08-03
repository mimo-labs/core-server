import logging

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.postgres.fields import JSONField

from common.validators import validate_path
from common.models import DateAwareModel


logger = logging.getLogger(__name__)


class Category(DateAwareModel):
    name = models.CharField(
        max_length=255
    )
    project = models.ForeignKey(
        'tenants.Project',
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = _('Categories')

    def __str__(self):
        return f"{self.name} (project id: {self.project.id})"


class Endpoint(DateAwareModel):
    path = models.CharField(
        max_length=2048,
        validators=(validate_path,),
        default='/'
    )
    categories = models.ManyToManyField(
        'mocks.Category',
        blank=True,
        related_name="endpoints",
    )

    def __str__(self):
        return self.path

    @property
    def project(self):
        return self.categories.first().project


class Content(DateAwareModel):
    content = JSONField(
        blank=True,
        default=dict
    )
    mock = models.ForeignKey(
        'mocks.Mock',
        null=True,
        unique=True,
        related_name='content',
        on_delete=models.CASCADE
    )


class Params(DateAwareModel):
    content = JSONField(
        blank=True,
        default=dict
    )
    mock = models.ForeignKey(
        'mocks.Mock',
        null=True,
        unique=True,
        related_name='params',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = _('Params')


class Mock(DateAwareModel):
    title = models.CharField(
        max_length=255,
        unique=True,
        null=True,
    )
    verb = models.ForeignKey(
        'mocks.HttpVerb',
        null=True,
        on_delete=models.PROTECT
    )
    path = models.ForeignKey(
        'mocks.Endpoint',
        null=True,
        on_delete=models.PROTECT
    )
    status_code = models.IntegerField(
        default=200
    )
    is_active = models.BooleanField(
        default=False
    )
    is_complete = models.BooleanField(
        default=False
    )

    @property
    def project(self):
        return self.path.project

    def save(self, *args, **kwargs):
        is_new = not self.pk
        if self.path and self.title:
            self.is_complete = True

        super().save(*args, **kwargs)

        if is_new:
            if not self.content.exists():
                logger.info(f'create default content for mock {self.pk}')
                Content.objects.create(
                    mock=self
                )
            if not self.params.exists():
                logger.info(f'create default params for mock {self.pk}')
                Params.objects.create(
                    mock=self
                )

        active_mocks = Mock.objects.exclude(id=self.pk).filter(
            path=self.path,
            is_active=True
        )

        if active_mocks.exists():
            active_mocks.update(is_active=False)

    def __str__(self):
        return self.title


class HeaderType(DateAwareModel):
    name = models.CharField(
        max_length=255,
    )
    organization = models.ForeignKey(
        'tenants.Organization',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.name


class Header(DateAwareModel):
    header_type = models.ForeignKey(
        'mocks.HeaderType',
        on_delete=models.CASCADE
    )
    value = models.TextField()
    mock = models.ForeignKey(
        "mocks.Mock",
        related_name="headers",
        on_delete=models.CASCADE
    )

    @property
    def as_response_header(self):
        return self.header_type.name, self.value

    @property
    def project(self):
        return self.mock.project

    def __str__(self):
        return "%s: %s" % (self.header_type, self.value)


class HttpVerb(DateAwareModel):
    name = models.CharField(
        max_length=255,
    )
    organization = models.ForeignKey(
        'tenants.Organization',
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        verbose_name = _('HTTP Verb')
        verbose_name_plural = _('HTTP Verbs')

    def __str__(self):
        return self.name
