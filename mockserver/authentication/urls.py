from rest_framework import routers

from authentication.views import Login, Logout


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'login', Login, base_name='login')
router.register(r'logout', Logout, base_name='logout')

urlpatterns = router.urls
