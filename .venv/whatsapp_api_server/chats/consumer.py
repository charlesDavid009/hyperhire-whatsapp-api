import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            chatroom_id = self.scope['url_route']['kwargs']['chatroom_id']
        except KeyError:
            return

        chatroom_group_name = f"chat_{chatroom_id}"
        await self.channel_layer.group_add(
            chatroom_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        chatroom_id = self.scope['url_route']['kwargs']['chatroom_id']
        chatroom_group_name = f"chat_{chatroom_id}"

        # Notify group about user disconnection
        await self.send_group_message({
            'type': 'chat.user_left',
            'user_id': self.scope['user'].id,  
        })

        # Leave chatroom group
        await self.channel_layer.group_discard(
            chatroom_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle different types of messages here based on your application logic
        # For example, you might have 'chat.message' and 'chat.attachment' types
        pass

    async def chat_message(self, event):
        message_id = event['message_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message_id': message_id,
        }))

    async def send_group_message(self, message):
        chatroom_id = self.scope['url_route']['kwargs']['chatroom_id']
        chatroom_group_name = f"chat_{chatroom_id}"

        # Send message to chatroom group
        await self.channel_layer.group_send(
            chatroom_group_name,
            message
        )

    async def chat_user_joined(self, event):
        user_id = event['user_id']
        # Handle user joined event (e.g., notify other users in the group)

    async def chat_user_left(self, event):
        user_id = event['user_id']
        # Handle user left event (e.g., notify other users in the group)
