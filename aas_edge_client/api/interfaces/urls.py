# urls.py or interfaces/urls.py
from rest_framework.routers import DefaultRouter
# from .views import InterfaceViewSet

from .views import NetworkSettingViewSet


router = DefaultRouter()
router.register(r'', NetworkSettingViewSet, basename='interface')

urlpatterns = router.urls
