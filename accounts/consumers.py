import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        m_type = data.get('type', 'chat_message')

        if m_type == 'chat_message':
            message_text = data['message']
            user = self.scope['user']
            msg_obj = await self.save_message(user, self.chat_id, message_text)
            
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'broadcast_message',
                'message': message_text,
                'sender': user.username,
                'msg_id': msg_obj.id
            })

        elif m_type == 'read_receipt':
            # Tell everyone in the group that this user has seen the messages
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'broadcast_read',
                'reader': self.scope['user'].username
            })

        elif m_type == 'typing':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'broadcast_typing',
                'sender': self.scope['user'].username,
                'is_typing': data['typing']
            })

    # Broadcast Handlers
    async def broadcast_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message', 
            'message': event['message'], 
            'sender': event['sender']
        }))

    async def broadcast_read(self, event):
        await self.send(text_data=json.dumps({
            'type': 'messages_read', 
            'reader': event['reader']
        }))

    async def broadcast_typing(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing', 
            'sender': event['sender'], 
            'is_typing': event['is_typing']
        }))

    @database_sync_to_async
    def save_message(self, user, chat_id, content):
        chat = Chat.objects.get(id=chat_id)
        return Message.objects.create(chat=chat, sender=user, content=content)
