from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from parser.views import index, refresh

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('refresh/', refresh),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
