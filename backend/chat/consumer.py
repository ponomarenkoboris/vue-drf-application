import json

from django.core.checks import messages 
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
from . import serializers

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        

        # Join room group

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        room = await self.get_chat_room()

        await self.send(text_data=json.dumps({'room': room}))

    
    async def disconnect(self, code):
        
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', None)
        sender = text_data_json.get('sender', None)

        if sender or message is None:
            # TODO procces error
            pass
        
        await self.post_message(sender=sender, message=message)
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': sender,
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event.get('message', None)
        sender = event.get('sender', None)

        if sender or message is None:
            # TODO procces error
            pass

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'sender': sender,
            'message': message
        }))

    @database_sync_to_async
    def get_chat_room(self):
        try:
            chat_room = ChatRoom.objects.get(room_name=self.room_name)
            return serializers.ChatRoomSerializer(chat_room).data

        except ObjectDoesNotExist:
            chat_room = ChatRoom.objects.create(room_name=self.room_name)
            return serializers.ChatRoomSerializer(chat_room).data


    @database_sync_to_async
    def post_message(self, sender, message):
        chat_room = ChatRoom.objects.get(room_name=self.room_name)
        Message.objects.create(room=chat_room, sender=sender, message=message)