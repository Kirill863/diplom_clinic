"""
Административная панель Django для системы управления клиникой.

Модуль регистрирует модели в административной панели и настраивает
их отображение, фильтрацию и функциональность для удобного управления
данными медицинского учреждения.
"""

from django.contrib import admin
from .models import Doctor, Service, Appointment, Testimonial, MedicalRecord
from django import forms

class DoctorAdminForm(forms.ModelForm):
    """
    Кастомная форма для модели Doctor с дополнительным полем пароля.
    
    Позволяет устанавливать или изменять пароль врача непосредственно
    в административной панели без использования стандартной системы пользователей.
    """
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Пароль")
    
    class Meta:
        model = Doctor
        fields = '__all__'

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для управления врачами.
    
    Включает:
    - Кастомную форму с полем пароля
    - Отображение основных полей в списке
    - Поиск по имени, специализации и логину
    - Фильтрацию по специализации
    - Хеширование пароля при сохранении
    """
    form = DoctorAdminForm
    list_display = ('name', 'specialization', 'experience', 'username')
    search_fields = ('name', 'specialization', 'username')
    list_filter = ('specialization',)
    
    def save_model(self, request, obj, form, change):
        """Переопределение метода сохранения для хеширования пароля."""
        if form.cleaned_data.get('password'):
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для управления медицинскими услугами.
    
    Включает:
    - Отображение названия, описания и порядка сортировки
    - Поиск по названию и описанию
    - Фильтрацию по порядку сортировки
    """
    list_display = ('title', 'description', "order")
    search_fields = ('title', 'description')
    list_filter = ('order',)    

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для управления записями на прием.
    
    Включает:
    - Отображение информации о пациенте, враче и времени записи
    - Фильтрацию по врачу и датам
    - Поиск по имени и телефону пациента
    - Иерархический навигатор по датам
    """
    list_display = ('name', 'phone', 'doctor', 'date', 'message', 'created_at')
    list_filter = ('doctor', 'date', 'created_at')
    search_fields = ('name', 'phone')
    date_hierarchy = 'date'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для управления отзывами пациентов.
    
    Включает:
    - Отображение основных полей отзыва
    - Фильтрацию по статусу одобрения, рейтингу и дате
    - Возможность быстрого редактирования статуса одобрения
    - Поиск по имени пациента, врачу и тексту отзыва
    - Группировку полей в логические блоки
    """
    list_display = ['name', 'doctor', 'rating', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'rating', 'created_at']
    list_editable = ['is_approved']
    search_fields = ['name', 'doctor', 'message']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Информация о пациенте', {
            'fields': ('name', 'doctor')
        }),
        ('Содержание отзыва', {
            'fields': ('message', 'rating')
        }),
        ('Статус', {
            'fields': ('is_approved', 'created_at')
        }),
    )

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для управления медицинскими картами.
    
    Включает:
    - Кастомное отображение информации о назначении
    - Фильтрацию по дате создания, врачу и услугам
    - Расширенный поиск по различным полям
    - Горизонтальный виджет для выбора услуг
    - Группировку полей в логические блоки
    - Кастомные методы для отображения связанных данных
    """
    list_display = ['appointment_info', 'doctor_name', 'created_at_short', 'services_list']
    list_filter = ['created_at', 'doctor', 'services']
    search_fields = [
        'appointment__name', 
        'appointment__phone',
        'diagnosis', 
        'treatment',
        'doctor__name'
    ]
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    filter_horizontal = ['services']
    
    def appointment_info(self, obj):
        """Форматированное отображение информации о пациенте."""
        return f"{obj.appointment.name} ({obj.appointment.phone})"
    appointment_info.short_description = 'Пациент'
    
    def doctor_name(self, obj):
        """Отображение имени врача."""
        return obj.doctor.name
    doctor_name.short_description = 'Врач'
    
    def created_at_short(self, obj):
        """Форматирование даты создания записи."""
        return obj.created_at.strftime("%d.%m.%Y %H:%M")
    created_at_short.short_description = 'Создано'
    
    def services_list(self, obj):
        """Отображение списка услуг через запятую."""
        return ", ".join([service.title for service in obj.services.all()])
    services_list.short_description = 'Услуги'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('appointment', 'doctor', 'created_at')
        }),
        ('Медицинская информация', {
            'fields': ('services', 'diagnosis', 'treatment', 'recommendations')
        }),
    )

# Настройка заголовка административной панели
admin.site.site_header = "Администрирование клиники"