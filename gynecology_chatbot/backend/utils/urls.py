from django.urls import path
from .views import health_check, redirect_to_admin, redirect_to_appointments
from .placeholder import placeholder_image

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('placeholder/<width>/<height>', placeholder_image, name='placeholder_image'),
    path('go-to-appointments/', redirect_to_appointments, name='go_to_appointments'),
]