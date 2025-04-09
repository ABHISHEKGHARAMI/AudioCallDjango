import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Check if user is authenticated
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()
            return

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'videocall_{self.room_name}'
        self.user = self.scope["user"]

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Notify room that a new user joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_join',
                'username': self.user.username,
                'sender_channel_name': self.channel_name
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Notify room that a user left
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_leave',
                'username': self.user.username,
                'sender_channel_name': self.channel_name
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        # Add username to the message
        data['username'] = self.user.username

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'signal_message',
                'message': data,
                'sender_channel_name': self.channel_name
            }
        )

    # User join notification
    async def user_join(self, event):
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({
                'type': 'user-joined',
                'username': event['username']
            }))

    # User leave notification
    async def user_leave(self, event):
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({
                'type': 'user-left',
                'username': event['username']
            }))

    # Receive message from room group
    async def signal_message(self, event):
        message = event['message']

        # Don't send the message back to the sender
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps(message))
