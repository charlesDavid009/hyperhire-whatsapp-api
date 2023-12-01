import json
from django.urls import reverse
from rest_framework import status
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from chats.consumer import ChatConsumer
from chats.entity.models import ChatRoom
from rest_framework.test import APIClient


class ChatroomTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.chatroom = ChatRoom.objects.create(name='Test Chatroom', max_members= '20')
        self.chatroom.members.add(self.user)

    def test_register_user(self):
        response = self.client.post('/api/createuser/', {'username': 'newuser', 'password': 'newpassword'})
        self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)

    def test_create_chatrooms(self):
        response = self.client.post('/api/chatrooms/', {'name': 'chatroom 1', 'max_members': '20'})
        self.assertEqual(response.status_code, 201)
        
    def test_list_chatrooms(self):
        response = self.client.get('/api/chatrooms/')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIsInstance(response_json, list)

    def test_send_message(self):
        url = reverse('message-list-create', kwargs={'chatroom_id': self.chatroom.id})
        data = {'text': 'Welcome to this room', 'chatroom': self.chatroom.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        
    def test_list_messages_by_chatroom_id(self):
        url = reverse('message-list-create', kwargs={'chatroom_id': self.chatroom.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
