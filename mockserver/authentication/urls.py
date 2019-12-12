from rest_framework import routers

from authentication.views import Login


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'login', Login, base_name='login')

urlpatterns = router.urls
