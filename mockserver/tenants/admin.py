from django.contrib import admin

from tenants.models import (
    Organization,
    Tenant,
    OrganizationMembership,
)


class PasswordHasherMixin(object):

    def save_model(self, request, obj, form, change, **kwargs):
        # Override this to set the password to the value in the field if it's
        # changed.
        if obj.pk:
            orig_obj = obj.__class__.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()


class OrganizationMembershipAdmin(admin.StackedInline):
    model = OrganizationMembership


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    fields = ('name', 'is_playground',)
    list_display = ('name', 'uuid',)


@admin.register(Tenant)
class TenantAdmin(PasswordHasherMixin, admin.ModelAdmin):
    inlines = (
        OrganizationMembershipAdmin,
    )
