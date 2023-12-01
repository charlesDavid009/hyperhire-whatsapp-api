from django.urls import path
from chats.controller.controllers import ChatRoomListCreateView, MessageListCreateView, AttachmentCreateView, LoginView, CreateUserView

urlpatterns = [
    path('chatrooms/', ChatRoomListCreateView.as_view(), name='chatroom-list-create'),
    path('messages/<int:chatroom_id>/', MessageListCreateView.as_view(), name='message-list-create'),
    path('attachments/', AttachmentCreateView.as_view(), name='attachment-create'),
    path('login/', LoginView.as_view(), name='login'),
    path('createuser/', CreateUserView.as_view(), name='create-user'),
]
