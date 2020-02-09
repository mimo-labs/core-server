from django.contrib import admin

# Register your models here.
from base.models import Technology


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    pass
