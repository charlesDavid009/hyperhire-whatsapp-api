import os
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

def upload_to(instance, filename):
    """
    Dynamic upload_to function to organize attachments based on type.
    """
    ext = filename.split('.')[-1]
    date_path = timezone.now().strftime('%Y/%m/%d')
    
    if instance.message.is_image_attachment():
        return os.path.join('attachments/pictures', date_path, f"{timezone.now().timestamp()}.{ext}")
    elif instance.message.is_video_attachment():
        return os.path.join('attachments/videos', date_path, f"{timezone.now().timestamp()}.{ext}")
    else:
        # Handle other attachment types as needed
        return os.path.join('attachments/other', date_path, f"{timezone.now().timestamp()}.{ext}")

class ChatRoom(models.Model):
    """
    Model representing a chat room.
    """
    name = models.CharField(max_length=255, unique=True)
    max_members = models.PositiveIntegerField(default=10)
    members = models.ManyToManyField(User, related_name='chat_rooms')

class Message(models.Model):
    """
    Model representing a chat message.
    """
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Attachment(models.Model):
    """
    Model representing an attachment in a chat message.
    """
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_to)

