from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('apps.main.urls')),
    path('api/', include('apps.api.urls')),
    # path('payme/', include('paymeuz.urls')),
    path('', include('apps.basic.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)