import uuid

from django.db import models
from django.template.defaultfilters import slugify

from authentication.models import User
from common.models import DateAwareModel
from tenants.constants import DEFAULT_PROJECT_CATEGORY_NAME
from tenants.tasks import mail_membership_invite
from mocks.models import Category


class Project(DateAwareModel):
    name = models.CharField(
        max_length=255
    )
    record_name = models.SlugField(
        max_length=255,  # RFC 1035
        null=True
    )
    organization = models.ForeignKey(
        'tenants.Organization',
        on_delete=models.CASCADE,
        null=True
    )

    def save(self, *args, **kwargs):
        self.record_name = slugify(self.name)
        project = super().save(*args, **kwargs)
        Category.objects.create(
            name=DEFAULT_PROJECT_CATEGORY_NAME,
            project=self,
        )

        return project

    def __str__(self):
        return self.name


class OrganizationMembership(DateAwareModel):
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE
    )
    organization = models.ForeignKey(
        'tenants.Organization',
        on_delete=models.CASCADE
    )
    is_owner = models.BooleanField(
        default=False
    )
    is_admin = models.BooleanField(
        default=False
    )

    class Meta:
        unique_together = (
            ('tenant', 'organization'),
            ('is_owner', 'organization'),
        )


class OrganizationProfile(models.Model):
    organization = models.OneToOneField(
        'tenants.Organization',
        related_name="profile",
        on_delete=models.CASCADE,
        null=True
    )

    public_name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    technologies = models.ManyToManyField(
        'base.Technology',
        blank=True
    )
    avatar = models.ImageField(default="default.png")
    website = models.URLField(null=True)
    twitter = models.CharField(max_length=512, null=True)
    facebook = models.CharField(max_length=512, null=True)
    linkedin = models.CharField(max_length=512, null=True)
    instagram = models.CharField(max_length=512, null=True)


class Organization(DateAwareModel):
    name = models.CharField(
        max_length=255
    )
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    is_playground = models.BooleanField(
        default=False
    )
    users = models.ManyToManyField(
        'tenants.Tenant',
        related_name="organizations",
        through=OrganizationMembership,
        blank=True
    )

    def save(self, **kwargs):
        is_new = not self.pk
        super(Organization, self).save(**kwargs)

        if is_new:
            OrganizationProfile.objects.create(
                organization=self,
                public_name=self.name
            )
            FeatureFlag.objects.create(
                organization=self,
            )

    @property
    def member_count(self):
        return self.organizationmembership_set.count()

    @property
    def mock_count(self):
        return self.mock_set.count()

    def __str__(self):
        return f"{self.name} ({self.uuid})"


class FeatureFlag(DateAwareModel):
    organization = models.OneToOneField(
        'tenants.Organization',
        related_name="feature_flags",
        on_delete=models.CASCADE,
        null=True
    )


class Tenant(DateAwareModel, User):
    pass


class OrganizationInvite(DateAwareModel):
    organization = models.ForeignKey(
        'tenants.Organization',
        on_delete=models.CASCADE,
        null=True
    )
    email = models.EmailField()
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.SET_NULL,
        null=True
    )
    from_domain = models.CharField(
        max_length=256,
        null=False,
        default="",
    )
    is_accepted = models.BooleanField(
        default=False
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            is_existing = self.tenant is not None
            mail_membership_invite.delay(is_existing, self.email, self.organization.name,
                                         self.from_domain)
