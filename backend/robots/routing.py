from django.urls import re_path

from . import websocket_consumer

websocket_urlpatterns = [
    re_path(r'ws/fault', websocket_consumer.SensorFailConsumer.as_asgi()),
]
