from django.urls import path
from .views import appointment_view

urlpatterns = [
    path('', appointment_view, name='appointments'),
]
