from rest_framework.routers import SimpleRouter

from mocks.views import (
    MockViewset,
    HeaderTypeViewset,
    HttpVerbViewset,
    EndpointViewset,
    CategoryViewset,
)
from tenants.views import (
    TenantViewSet,
    OrganizationViewSet,
    ProjectViewset,
)

app_name = 'api'


router = SimpleRouter()
router.register('tenants', TenantViewSet)
router.register('organizations', OrganizationViewSet)
router.register('mocks', MockViewset)
router.register('header-types', HeaderTypeViewset)
router.register('http-verbs', HttpVerbViewset)
router.register('categories', CategoryViewset)
router.register('endpoints', EndpointViewset)
router.register('projects', ProjectViewset)

urlpatterns = router.urls
