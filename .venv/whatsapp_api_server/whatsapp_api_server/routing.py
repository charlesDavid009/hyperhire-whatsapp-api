# asgi.py or routing.py (project level)
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack
from chats.consumer import ChatConsumer
from chats.routing import websocket_urlpatterns 

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path("ws/chat/", ChatConsumer.as_asgi()),
            ] +
            websocket_urlpatterns  
        )
    ),
})
