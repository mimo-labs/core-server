from django.urls import re_path

from api.views import fetch_mock


urlpatterns = [
    re_path(r"^.*/$", fetch_mock)
]
