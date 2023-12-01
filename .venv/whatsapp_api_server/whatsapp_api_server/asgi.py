"""
ASGI config for whatsapp_api_server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from .routing import application as chat_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whatsapp_api_server.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": chat_application,
})