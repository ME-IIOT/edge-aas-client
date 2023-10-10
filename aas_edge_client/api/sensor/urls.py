# urls.py or interfaces/urls.py
from rest_framework.routers import DefaultRouter
# from .views import InterfaceViewSet

from .views import SensorsViewSet


router = DefaultRouter()
router.register(r'', SensorsViewSet, basename='sensor')

urlpatterns = router.urls
