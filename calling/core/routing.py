from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from video.consumers import VideoCallConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/video/<str:room_name>/', VideoCallConsumer.as_asgi()),
        ])
    ),
})
