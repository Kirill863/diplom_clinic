from django.contrib import admin
from django.conf.urls.static import static 
from django.urls import path
from clinic import settings
from core.views import home  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)