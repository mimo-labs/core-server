from django.contrib import admin
from mocks.models import Mock, HeaderType, Header, HttpVerb


class HeaderInline(admin.TabularInline):
    extra = 0
    model = Header


@admin.register(Mock)
class MockAdmin(admin.ModelAdmin):
    inlines = [
        HeaderInline
    ]
    list_display = ('title', 'path', 'is_active')


admin.site.register(HttpVerb)


admin.site.register(HeaderType)
