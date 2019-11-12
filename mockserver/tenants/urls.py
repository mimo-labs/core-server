from django.urls import re_path

from tenants.views import fetch_mock


urlpatterns = [
    re_path(r"^.*/$", fetch_mock)
]
