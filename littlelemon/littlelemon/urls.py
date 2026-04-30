"""littlelemon URL configuration."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.static import serve as static_serve
from django.http import FileResponse
from pathlib import Path


def serve_sw(request):
    """Serve service worker from root scope (required for site-wide control)."""
    sw_path = Path(settings.BASE_DIR) / 'restaurant' / 'static' / 'sw.js'
    response = FileResponse(open(sw_path, 'rb'), content_type='application/javascript')
    response['Service-Worker-Allowed'] = '/'
    return response


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sw.js', serve_sw, name='service_worker'),
    path('offline.html', TemplateView.as_view(template_name='offline.html'), name='offline'),
    path('', include('restaurant.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
