from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "username", "name", "profile_picture")
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'font-sans text-sm'}),
        }

class CustomUserChangeForm(UserChangeForm):
    # Removes the password field/help text from the form display
    password = None 

    class Meta:
        model = CustomUser
        # Only show fields the user should edit on the frontend
        fields = ("email", "name", "profile_picture")
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'font-sans text-sm'}),
        }
