"""
URL configuration for backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.generic import RedirectView

def health_check(request):
    """Simple health check endpoint."""
    return JsonResponse({
        'status': 'ok',
        'message': 'Chemical Equipment Intelligence API is running',
        'api_endpoint': '/api/'
    })

urlpatterns = [
    path('', health_check, name='health_check'),  # Root URL
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
