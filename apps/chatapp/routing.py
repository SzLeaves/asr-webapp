from channels.auth import AuthMiddlewareStack
from django.urls import re_path

from chatapp.consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r'^chatapp/ws/$', AuthMiddlewareStack(ChatConsumer.as_asgi())),
    re_path(
        r'^chatapp/ws/(?P<session_id>[0-9a-f]{8}-[0-9a-f]{4}-1[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})/$',
        AuthMiddlewareStack(ChatConsumer.as_asgi())
    ),
]
