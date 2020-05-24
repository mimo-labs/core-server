from django.contrib import admin

from mocks.models import (
    HeaderType,
    HttpVerb,
    Endpoint,
    Category,
)


# class HeaderInline(admin.TabularInline):
#     extra = 0
#     model = Header
#
#
# class ParamsInline(admin.TabularInline):
#     extra = 0
#     model = Params
#
#
# class ContentInline(admin.TabularInline):
#     extra = 0
#     model = Content
#
#
# @admin.register(Mock)
# class MockAdmin(admin.ModelAdmin):
#     inlines = [
#         HeaderInline,
#         ParamsInline,
#         ContentInline,
#     ]
#     list_display = ('title', 'path', 'is_active')


admin.site.register(HttpVerb)
admin.site.register(Endpoint)
admin.site.register(Category)


admin.site.register(HeaderType)
