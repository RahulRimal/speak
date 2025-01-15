from channels.generic.websocket import AsyncWebsocketConsumer
import json


class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "rooms"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive a message from WebSocket
    async def receive(self, text_data):
        # Handle messages from WebSocket if needed
        pass

    # Broadcast new room
    async def new_room(self, event):
        action = "add_room"
        room_data = event["event_data"]
        await self.send(text_data=json.dumps({"action": action, **room_data}))

    async def remove_room(self, event):
        action = "remove_room"
        room_id = event["room_id"]
        await self.send(text_data=json.dumps({"action": action, "room_id": room_id}))


class AudioRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"room_{self.room_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action in [
            "webrtc_offer",
            "webrtc_answer",
            "webrtc_ice_candidate",
            "mute_update",
        ]:
            data["sender_channel_name"] = self.channel_name
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "webrtc_signal", **data}
            )

    async def webrtc_signal(self, event):
        # Don't send the message back to the sender
        if (event["sender_channel_name"] != self.channel_name):
            await self.send(text_data=json.dumps(event))
            return

        # But if it's the audio mute case, send it to the same client too to update the UI
        if event["action"] == "mute_update":
            await self.send(text_data=json.dumps(event))

    async def join_room(self, event):
        action = "join_room"
        data = event.get("event_data")
        await self.send(text_data=json.dumps({"action": action, **data}))

    async def leave_room(self, event):
        action = "leave_room"
        data = event.get("event_data")
        await self.send(text_data=json.dumps({"action": action, **data}))

    async def room_event(self, event):
        action = event["action"]
        username = event["username"]
        image_url = event.get("image_url")
        room_id = event.get("room_id")

        await self.send(
            text_data=json.dumps(
                {
                    "action": action,
                    "username": username,
                    "image_url": image_url,
                    "room_id": room_id,
                }
            )
        )
