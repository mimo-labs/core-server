from django.contrib import admin
from core.models import Mock, HeaderType, Header


class HeaderInline(admin.TabularInline):
    extra = 0
    model = Header


@admin.register(Mock)
class MockAdmin(admin.ModelAdmin):
    inlines = [
        HeaderInline
    ]


admin.site.register(HeaderType)
