from django.urls import re_path
from chat import consumers

websocket_urlpatterns = [
    # url(r'^ws/msg/(?P<room_name>[^/]+)/$', consumers.SyncConsumer),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.AsyncConsumer),
]