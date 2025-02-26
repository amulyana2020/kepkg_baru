
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('dashboard/', include('app.urls')),
    path('accounts/', include('django.contrib.auth.urls'), name='login'),
    path('select2/', include('django_select2.urls')),
    path('register/', register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

