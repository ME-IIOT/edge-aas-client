# urls.py or interfaces/urls.py
from rest_framework.routers import DefaultRouter
from .views import InterfaceViewSet

router = DefaultRouter()
router.register(r'interfaces', InterfaceViewSet, basename='interface')

urlpatterns = router.urls
