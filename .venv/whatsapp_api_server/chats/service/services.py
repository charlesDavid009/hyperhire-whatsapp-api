from django.contrib.auth.models import User
from chats.repository.repository import ChatRepository, MessageRepository, AttachmentRepository
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from chats.entity.models import ChatRoom, Message, Attachment

class ChatService:
    """
    Service for chat room business logic.
    """
    def get_chatrooms(self):
        """
        Get a list of chat rooms.
        """
        return ChatRepository().get_chatrooms()

    def create_chatroom(self, name, max_members):
        """
        Create a new chat room.
        """
        return ChatRepository().create_chatroom(name, max_members)

    def leave_chatroom(self, user, chatroom):
        """
        Leave a chat room.
        """
        ChatRepository().leave_chatroom(user, chatroom)

    def get_user_chatrooms(self, user):
        """
        Get a list of user chat rooms.
        """
        return user.chat_rooms.all()
    
    def join_chatroom(self, user, chatroom):
        """
        Join a chat room.
        """
        ChatRepository().join_chatroom(user, chatroom)

class MessageService:
    """
    Service for message business logic.
    """
    def get_messages(self, chatroom):
        """
        Get messages for a chat room.
        """
        return MessageRepository().get_messages(chatroom)

    def create_message(self, chatroom, sender, text):
        """
        create and send message into a chat room
        """
        return MessageRepository().create_message(sender, text, chatroom)
        
class AttachmentService:
    """
    Service for attachment business logic.
    """
    def create_attachment(self, message, file):
        """
        Create a new attachment.
        """
        return AttachmentRepository().create_attachment(message, file)
