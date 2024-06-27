from django.urls import path
from .consumers import DashboardConsumer

websocket_urlpatterns = [
    path('ws/sensor-data/', DashboardConsumer.as_asgi()),
]