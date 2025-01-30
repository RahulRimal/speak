from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Participant, Room


def home(request):
    rooms = Room.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "communicate/home.html", {"rooms": rooms})


@login_required(login_url="login")
def create_room(request):
    if request.method == "POST":
        room_name = request.POST.get("name")
        if room_name:
            room = Room.objects.create(name=room_name, host=request.user)
            participant = Participant.objects.create(user=request.user, room=room)

            # Notify WebSocket about the new room
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "rooms",
                {
                    "type": "new_room",
                    "event_data": {
                        "id": room.id,
                        "name": room.name,
                        "host_username": room.host.username,
                        "participants": [
                            {
                                "username": participant.user.username,
                                "image_url": (
                                    participant.user.image.url
                                    if participant.user.image
                                    else None
                                ),
                                "first_name": participant.user.first_name,
                                "last_name": participant.user.last_name,
                            }
                            
                        ],
                    },
                },
            )

            return redirect("room_detail", room_id=room.id)
    return render(request, "communicate/create_room.html")


def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, "communicate/room_detail.html", {"room": room})


@login_required(login_url="login")
def join_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if not Participant.objects.filter(user=request.user, room=room).exists():
        # Create a new participant
        participant = Participant.objects.create(user=request.user, room=room)

        # Notify via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"room_{room.id}",
            {
                "type": "join_room",
                "event_data": {
                    "username": participant.user.username,
                    "image_url": participant.user.image.url if participant.user.image else None,
                },
            },
        )

    return redirect("room_detail", room_id=room.id)


@login_required(login_url="login")
def leave_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    participant = get_object_or_404(Participant, user=request.user, room=room)

    participant.delete()

    # Notify via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"room_{room.id}",
        {
            "type": "leave_room",
            "event_data": {
                "username": participant.user.username,
            },
        },
    )

    if room.participants.count() == 0:
        async_to_sync(channel_layer.group_send)(
            "rooms",
            {
                "type": "remove_room",
                "room_id": room.id,
            },
        )

        # Delete the room if there are no participants
        room.delete()

    return redirect("home")
