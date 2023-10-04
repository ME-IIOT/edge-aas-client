from django.urls import path, include

urlpatterns = [
    path('interfaces/', include('api.interfaces.urls')),
    path('templates/', include('api.template.urls')),
    # Add more paths as needed
]
