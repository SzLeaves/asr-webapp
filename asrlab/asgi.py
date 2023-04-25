import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asrlab.settings')
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from chatapp.routing import websocket_urlpatterns


# 支持http请求和websocket请求
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns)
})
