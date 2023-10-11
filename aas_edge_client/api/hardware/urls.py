from rest_framework.routers import DefaultRouter

from .views import HardwareViewSet

router = DefaultRouter()
router.register(r'', HardwareViewSet, basename='hardware')

urlpatterns = router.urls