from rest_framework.routers import SimpleRouter

from tenants.views import (
    TenantViewSet,
    OrganizationViewSet
)

app_name = 'tenants'

router = SimpleRouter()
router.register('tenants', TenantViewSet)
router.register('organizations', OrganizationViewSet)

urlpatterns = router.urls
