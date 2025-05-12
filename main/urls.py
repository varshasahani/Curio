from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('curio.urls')),  # Include the URLs from the curio app
    path('', include('glance.urls')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)