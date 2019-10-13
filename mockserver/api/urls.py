from rest_framework import routers

from api.views import MockViewset

router = routers.SimpleRouter()
router.register('mocks', MockViewset)

urlpatterns = router.urls
