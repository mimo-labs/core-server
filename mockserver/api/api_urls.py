from rest_framework.routers import SimpleRouter

from mocks.views import (
    MockViewset,
    HeaderTypeViewset,
    HeaderViewset,
    HttpVerbViewset,
    EndpointViewset,
    CategoryViewset,
    ProjectViewset,
)
from tenants.views import (
    TenantViewSet,
    OrganizationViewSet
)

app_name = 'api'


router = SimpleRouter()
router.register('tenants', TenantViewSet)
router.register('organizations', OrganizationViewSet)
router.register('mocks', MockViewset)
router.register('header-types', HeaderTypeViewset)
router.register('headers', HeaderViewset)
router.register('http-verbs', HttpVerbViewset)
router.register('categories', CategoryViewset)
router.register('endpoints', EndpointViewset)
router.register('projects', ProjectViewset)

urlpatterns = router.urls
