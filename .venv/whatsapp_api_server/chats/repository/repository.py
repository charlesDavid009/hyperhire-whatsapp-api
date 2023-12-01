from chats.entity.models import ChatRoom, Message, Attachment
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class ChatRepository:
    """
    Repository for chat room operations.
    """
    def get_chatrooms(self):
        """
        Get a list of chat rooms.
        """
        return ChatRoom.objects.all()

    def create_chatroom(self, name, max_members):
        """
        Create a new chat room.
        """
        return ChatRoom.objects.create(name=name, max_members=max_members)

    def leave_chatroom(self, user, chatroom):
        """
        Leave a chat room.
        """
        chatroom.members.remove(user)
        
    def join_chatroom(self, user, chatroom):
        """
        Join a chat room.
        """
        chatroom.members.add(user)

class MessageRepository:
    """
    Repository for message operations.
    """
    def get_messages(self, chatroom):
        """
        Get messages for a chat room.
        """
        return Message.objects.filter(chatroom=chatroom)
    
    def create_message(self, sender, text, chatroom):
        # Create and save the message
        message = Message(chatroom=chatroom, sender=sender, text=text)
        message.save()

        # Notify consumers about the new message
        #self.notify_consumers(chatroom.id, message.id)
        return message
    
    def notify_consumers(self, chatroom_id, message_id):


        channel_layer = get_channel_layer()
        chatroom_group_name = f"chat_{chatroom_id}"

        async_to_sync(channel_layer.group_send)(
            chatroom_group_name,
            {
                'type': 'chat.message',
                'message_id': message_id,
            }
        )

class AttachmentRepository:
    """
    Repository for attachment operations.
    """
    def create_attachment(self, message, file):
        """
        Create a new attachment.
        """
        return Attachment.objects.create(message=message, file=file)
