"""
URL configuration for armentamj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://djangoproject.com
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static

# Global patterns that should not have a language prefix
urlpatterns = [
    # Built-in view to handle the language switching form logic
    path('i18n/', include('django.conf.urls.i18n')),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Patterns wrapped in i18n_patterns will automatically include the language prefix
urlpatterns += i18n_patterns(
    # Django Administration portal
    path('admin/', admin.site.urls),
    
    # Main entry point for the website
    path('', include('homepage.urls')),
    
    # Weather application logic
    path('weather/', include('weather.urls')),

    # Moved __reload__ inside i18n_patterns to prevent redirect loops/security errors
    path("__reload__/", include("django_browser_reload.urls")),
    
    # Force the language prefix even for the default language
    prefix_default_language=False
)

