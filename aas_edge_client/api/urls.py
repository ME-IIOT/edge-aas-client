from django.urls import path, include

urlpatterns = [
    # path('interfaces/', include('api.interfaces.urls')),
    # path('sensors/', include('api.sensor.urls')),
    # path('hardware/', include('api.hardware.urls')),
    path('NetworkConfiguration/', include('api.NetworkConfiguration.urls')),
    path('SystemInformation/', include('api.SystemInformation.urls')),
    # Add more paths as needed
]
