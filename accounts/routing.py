from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # This captures the chat ID from the URL so we know which room to join.
    # The 'chat_id' will be passed to the Consumer.
    re_path(r'ws/chat/(?P<chat_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
