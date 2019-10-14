from django.urls import re_path
from rest_framework import routers

from mocks.views import fetch_mock, MockViewset, HeaderTypeViewset, HttpVerbViewset


router = routers.SimpleRouter()
router.register('mocks', MockViewset)
router.register('header-types', HeaderTypeViewset)
router.register('http-verbs', HttpVerbViewset)


urlpatterns = [
    re_path(r"^.*/$", fetch_mock)
]
