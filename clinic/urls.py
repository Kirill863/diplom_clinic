from django.contrib import admin
from django.conf.urls.static import static 
from django.urls import path
from clinic import settings
from core.views import appointment_success, home, appointment_view, add_testimonial, all_testimonials, staff_login


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('appointment/', appointment_view, name='appointment'),
    path('appointment/success/', appointment_success, name='appointment_success'),
    path('testimonials/add/', add_testimonial, name='add_testimonial'),
    path('testimonials/all/', all_testimonials, name='all_testimonials'),
    path('staff/login/', staff_login, name='staff_login'),  

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)