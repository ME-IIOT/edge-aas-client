from django.urls import path
from .views import RetrievePeriodicTaskView  # Adjust the import path based on your project structure

urlpatterns = [
    path('', RetrievePeriodicTaskView.as_view(), name='retrieve-periodic-task'),
]
