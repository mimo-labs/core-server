from django.contrib import admin
from django.contrib.postgres import forms as pg_forms
from django import forms

from mocks.models import (
    HeaderType,
    HttpVerb,
    Endpoint,
    Category,
    Header,
    Params,
    Content,
    Mock,
)


class MockForm(forms.ModelForm):
    mock_content = pg_forms.JSONField(initial=dict, required=False)
    mock_params = pg_forms.JSONField(initial=dict, required=False)

    class Meta:
        model = Mock
        fields = (
            'title',
            'path',
            'verb',
            'status_code',
            'is_active',
            'mock_content',
            'mock_params',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get('instance')

        if instance:
            mock_content = instance.content.get().content
            mock_params = instance.params.get().content

            if mock_content:
                self.fields['mock_content'].initial = mock_content
                self.fields['mock_params'].initial = mock_params

    def save(self, commit=True):
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )

        instance = super().save(commit=True)

        content_data = self.cleaned_data.pop('mock_content')
        params_data = self.cleaned_data.pop('mock_params')

        content = instance.content.get()
        params = instance.params.get()

        if content_data:
            content.content = content_data
            content.save()

        if params_data:
            params.content = params_data
            params.save()

        self.save_m2m = self._save_m2m

        return instance


class HeaderInline(admin.TabularInline):
    extra = 0
    model = Header


class ParamsInline(admin.TabularInline):
    extra = 0
    model = Params


class ContentInline(admin.TabularInline):
    extra = 0
    model = Content


@admin.register(Mock)
class MockAdmin(admin.ModelAdmin):
    inlines = [
        HeaderInline,
    ]
    form = MockForm
    list_display = ('title', 'path', 'is_active')


admin.site.register(HttpVerb)
admin.site.register(Endpoint)
admin.site.register(Category)
# admin.site.register(Project)


admin.site.register(HeaderType)
