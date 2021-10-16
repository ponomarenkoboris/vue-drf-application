from rest_framework import serializers
from .models import ChatRoom, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'message', 'message_send_date']

class ChatRoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)
    
    class Meta:
        model = ChatRoom
        fields = ['room_name', 'messages']
