from rest_framework import routers

from mocks.views import (
    MockViewset,
    HeaderTypeViewset,
    HttpVerbViewset,
    CategoryViewset,
    EndpointViewset
)

router = routers.SimpleRouter()
router.register('mocks', MockViewset)
router.register('header-types', HeaderTypeViewset)
router.register('http-verbs', HttpVerbViewset)
router.register('categories', CategoryViewset)
router.register('endpoints', EndpointViewset)


urlpatterns = router.urls
