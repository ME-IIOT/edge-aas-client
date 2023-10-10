from django.urls import path, include

urlpatterns = [
    path('interfaces/', include('api.interfaces.urls')),
    path('sensors/', include('api.sensor.urls')),
    # Add more paths as needed
]
