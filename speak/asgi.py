from django.core.asgi import get_asgi_application
from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from communicate.consumers import AudioRoomConsumer, RoomConsumer

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("ws/room/<int:room_id>/", AudioRoomConsumer.as_asgi()),
                    path("ws/rooms/", RoomConsumer.as_asgi()),
                ]
            )
        ),
    }
)
