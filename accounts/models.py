from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    
    # Using CharField for the name. 
    # By default, blank=False and null=False, making it mandatory.
    name = models.CharField(max_length=100, unique=True)

    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    USERNAME_FIELD = 'email'
    
    # Since 'name' is now mandatory, you must add it to REQUIRED_FIELDS 
    # so Django prompts for it when you create a superuser.
    REQUIRED_FIELDS = ['username', 'name']

    def __str__(self):
        return self.email

from django.db import models
from django.conf import settings

class Chat(models.Model):
    # This allows 2, 3, or many people to be in one chat.
    # 'related_name' lets you do 'user.chats.all()' to find a user's threads.
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='chats'
    )
    
    # Optional name for group chats (blank/null for 1:1)
    name = models.CharField(max_length=255, blank=True, null=True)
    
    # Track when the conversation started
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Track the last message activity
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.name:
            return self.name
        return f"Chat with {self.participants.count()} people"

from django.core.validators import MinLengthValidator

class Message(models.Model):
    # Links this message to a specific conversation
    chat = models.ForeignKey(
        'Chat', 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    
    # Identifies who sent the message
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )
    
    # The actual text content (must be at least 1 character)
    content = models.TextField(validators=[MinLengthValidator(1)])
    
    # Automatically records when the message was created
    timestamp = models.DateTimeField(auto_now_add=True)

    # Tracks if the message has been seen by other participants
    # default=False ensures new messages start as 'unread'
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"

    class Meta:
        # Ensures messages are always retrieved in chronological order
        ordering = ['timestamp']