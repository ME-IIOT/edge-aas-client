from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import NetworkConfigurationViewSet

router = DefaultRouter()
router.register(r'', NetworkConfigurationViewSet, basename='NetworkConfiguration')

urlpatterns = router.urls

