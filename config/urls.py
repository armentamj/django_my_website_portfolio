"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # Adding User authentication and any other 1st of 2 steps for this page
from django.conf import settings # Import settings
from django.conf.urls.static import static # Import static helper
from accounts.views import home, signup, profile, edit_profile
from accounts import views  # Use your actual app name here


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # Adding User authentication 2nd of 2 steps on this page
    path('accounts/signup/', signup, name='signup'), # Adding the sign up route
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/edit/', edit_profile, name='edit_profile'), # For editing the user profiles
    path('', home, name='home'), #This is the 'root to: "home#index"'
    path('weather/', views.weather, name='weather'),
    path('chat_index/', views.chat_index, name='chat_index'),
    path('messages/<slug:slug>/', views.message_index, name='message_index')
]

# This serves media files (like profile pictures) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)