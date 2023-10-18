from rest_framework.routers import DefaultRouter

from .views import NetworkConfigurationViewSet

router = DefaultRouter()
router.register(r'', NetworkConfigurationViewSet, basename='NetworkConfiguration')

urlpatterns = router.urls
