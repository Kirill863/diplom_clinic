"""
URL Configuration for clinic project.

Данный модуль определяет маршруты URL для веб-приложения клиники.
Включает endpoints для административной панели, записей на прием, 
отзывов пациентов, аутентификации медицинского персонала и 
управления медицинскими картами.
"""

from django.contrib import admin
from django.conf.urls.static import static 
from django.urls import path
from clinic import settings
from core.views import (
    appointment_success, 
    home, 
    appointment_view, 
    add_testimonial, 
    all_testimonials, 
    staff_login, 
    doctor_login, 
    doctor_dashboard, 
    doctor_logout, 
    patient_card, 
    create_medical_record, 
    medical_records_list
)

# Основные URL patterns приложения
urlpatterns = [
    # Административная панель Django
    path('admin/', admin.site.urls),
    
    # Главная страница
    path('', home, name='home'),
    
    # Запись на прием
    path('appointment/', appointment_view, name='appointment'),
    path('appointment/success/', appointment_success, name='appointment_success'),
    
    # Отзывы пациентов
    path('testimonials/add/', add_testimonial, name='add_testimonial'),
    path('testimonials/all/', all_testimonials, name='all_testimonials'),
    
    # Аутентификация персонала
    path('staff/login/', staff_login, name='staff_login'), 
    path('doctor/login/', doctor_login, name='doctor_login'),
    path('doctor/dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('doctor/logout/', doctor_logout, name='doctor_logout'),    
    
    # Медицинские карты и записи
    path('patient-card/<int:appointment_id>/', patient_card, name='patient_card'),
    path('appointment/<int:appointment_id>/create-record/', create_medical_record, name='create_medical_record'),
    path('appointment/<int:appointment_id>/medical-records/', medical_records_list, name='medical_records_list'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)