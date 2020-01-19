from rest_framework.routers import SimpleRouter

from tenants.views import TenantViewSet

app_name = 'tenants'

router = SimpleRouter()
router.register('tenants', TenantViewSet)

urlpatterns = router.urls
