from rest_framework import routers

from mocks.views import MockViewset, HeaderTypeViewset, HttpVerbViewset


router = routers.SimpleRouter()
router.register('mocks', MockViewset)
router.register('header-types', HeaderTypeViewset)
router.register('http-verbs', HttpVerbViewset)


urlpatterns = router.urls
