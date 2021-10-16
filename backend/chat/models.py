from django.db import models

class ChatRoom(models.Model):
    room_name = models.CharField(max_length=255)

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE, null=True)
    sender = models.CharField(max_length=255)
    message = models.TextField(blank=False)
    message_send_date = models.DateTimeField(auto_now_add=True)