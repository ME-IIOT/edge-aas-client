from rest_framework.routers import DefaultRouter

from .views import SystemInformationViewSet

router = DefaultRouter()
router.register(r'', SystemInformationViewSet, basename='SystemInformation')

urlpatterns = router.urls