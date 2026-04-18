"""
URL configuration for armentamj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://djangoproject.com
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

# Global patterns that should not have a language prefix (e.g., /en/ or /de/)
# This includes the internal language switcher and the browser reloader
urlpatterns = [
    # Built-in view to handle the language switching form logic
    path('i18n/', include('django.conf.urls.i18n')),
]

# Patterns wrapped in i18n_patterns will automatically include the language prefix
# For example: /de/admin/ or /en/weather/
urlpatterns += i18n_patterns(
    # Django Administration portal
    path('admin/', admin.site.urls),
    
    # Main entry point for the website (landing page, portfolio, etc.)
    path('', include('homepage.urls')),
    
    # Weather application logic
    path('weather/', include('weather.urls')),
    
    # Force the language prefix even for the default language to ensure consistent routing
    prefix_default_language=True 
)

# Development-only patterns
if settings.DEBUG:
    # URL for the django-browser-reload package to handle hot-reloading during Tailwind development
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
