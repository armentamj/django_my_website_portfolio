import os
# Standard Django helper to handle regular HTTP traffic (HTML pages, APIs)
from django.core.asgi import get_asgi_application
# ProtocolTypeRouter: A "switchboard" that directs traffic based on its type (HTTP vs WebSocket)
# URLRouter: Similar to Django's urls.py, but specifically for WebSocket paths
from channels.routing import ProtocolTypeRouter, URLRouter
# AuthMiddlewareStack: Connects Django's authentication system to the WebSocket 
# so you can use 'self.scope["user"]' to see who is logged in
from channels.auth import AuthMiddlewareStack

# Imports the websocket_urlpatterns we will define in your accounts app
import accounts.routing

# Tells the server which settings file to use for the project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# The main application object that the server (Daphne) will run
application = ProtocolTypeRouter({
    
    # "http": If the connection is a standard web request, use the default Django logic
    "http": get_asgi_application(),
    
    # "websocket": If the connection is a WebSocket (ws://), use this logic
    "websocket": AuthMiddlewareStack(
        # URLRouter takes the list of paths from your accounts/routing.py
        URLRouter(
            accounts.routing.websocket_urlpatterns
        )
    ),
})
