from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    ChatRoomSerializer,
    MessageSerializer,
    AttachmentSerializer,
    UserProfileSerializer,
    LoginSerializer,
    TokenSerializer
)
from chats.service.services import ChatService, MessageService, AttachmentService
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from chats.entity.models import ChatRoom, Message
from drf_yasg.utils import swagger_auto_schema


class ChatRoomListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for creating and listing chat rooms.

    - To create a new chat room, send a POST request with the required parameters.
    - To list all chat rooms, send a GET request.

    Parameters (POST):
    - name: String, required, unique name for the chat room.
    - max_members: Integer, optional, maximum members allowed in the chat room (default is 10).

    Example (POST):
    {
        "name": "New Chat Room",
        "max_members": 20
    }

    Example (GET):
    GET /chatrooms/
    """
    serializer_class = ChatRoomSerializer
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: ChatRoomSerializer(many=True)})
    def get_queryset(self):
        """
        Get the list of chat rooms.

        Returns:
            QuerySet: List of chat rooms.
        """
        
        return ChatService().get_chatrooms()

    @swagger_auto_schema(request_body=ChatRoomSerializer)
    def create(self, request, *args, **kwargs):
    
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        max_members = serializer.validated_data.get('max_members', 10)
        if max_members < 2:
            return Response({'error': 'Max members should be at least 2.'}, status=status.HTTP_400_BAD_REQUEST)

        chatroom = ChatService().create_chatroom(serializer.validated_data['name'], max_members)
        ChatService().join_chatroom(request.user, chatroom)

        headers = self.get_success_headers(serializer.data)
        return Response(self.get_serializer(chatroom).data, status=status.HTTP_201_CREATED, headers=headers)


class MessageListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for creating and listing messages in a chat room.

    - To create a new message, send a POST request with the required parameters.
    - To list all messages in a chat room, send a GET request.

    Parameters (POST):
    - chatroom_id: Integer, required, ID of the chat room where the message will be posted.
    - text: String, required, text content of the message.

    Example (POST):
    {
        "chatroom_id": 1,
        "text": "Hello, World!"
    }

    Example (GET):
    GET /messages/1/
    """
    serializer_class = MessageSerializer
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: MessageSerializer(many=True)})
    def get_queryset(self):
        chatroom_id = self.kwargs.get('chatroom_id')
        try:
            chatroom = ChatRoom.objects.get(pk=chatroom_id)
            messages = MessageService().get_messages(chatroom)
            return messages
        except ChatRoom.DoesNotExist:
            return Message.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=MessageSerializer)
    def create(self, request, *args, **kwargs):
        chatroom_id = request.data.get('chatroom')
        text = request.data.get('text')

        try:
            chatroom = ChatRoom.objects.get(pk=chatroom_id)
        except ChatRoom.DoesNotExist:
            return Response({'error': 'Chat room does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the authenticated user (assuming user is logged in)
        sender = self.request.user 

        try:
            message = MessageService().create_message(chatroom, sender, text)
            serializer = self.get_serializer(message)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API endpoint for user login.

    - To log in, send a POST request with the username and password.

    Parameters (POST):
    - username: String, required, the username of the user.
    - password: String, required, the password of the user.

    Example (POST):
    {
        "username": "williams",
        "password": "password"
    }
    """

    @swagger_auto_schema(request_body=LoginSerializer, responses={status.HTTP_200_OK: TokenSerializer()})
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response(TokenSerializer(token).data)

class CreateUserView(generics.CreateAPIView):
    """
    API endpoint for creating a new user.

    Parameters:
        username (str): Username of the new user.
        password (str): Password of the new user.

    Returns:
        Response: Created user details.
    """

    serializer_class = UserProfileSerializer

    @swagger_auto_schema(request_body=MessageSerializer)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(self.get_serializer(user).data, status=status.HTTP_201_CREATED, headers=headers)


class AttachmentCreateView(generics.CreateAPIView):
    """
    API endpoint for creating attachments in a message.

    - To create a new attachment, send a POST request with the required parameters.

    Parameters (POST):
    - message_id: Integer, required, ID of the message where the attachment will be added.
    - file: File, required, the attachment file.

    Example (POST):
    {
        "message_id": 1,
        "file": <attach your file here>
    }
    """
    serializer_class = AttachmentSerializer
    
    @swagger_auto_schema(request_body=AttachmentSerializer)
    def create(self, request, *args, **kwargs):
        message_id = request.data.get('message_id')
        file = request.data.get('file')

        # Retrieve the message
        try:
            message = Message.objects.get(pk=message_id)
        except Message.DoesNotExist:
            return Response({'error': 'Message does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # Call AttachmentService to create attachment
        attachment_service = AttachmentService()
        attachment = attachment_service.create_attachment(message, file)

        serializer = self.get_serializer(attachment)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)