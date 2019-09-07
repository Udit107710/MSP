from django.urls import path
from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<room_name>/<user_name>/', consumers.ChatConsumer),
]