from django.contrib import admin
from .models import Doctor, Service, Appointment, Testimonial, MedicalRecord  # Добавили MedicalRecord
from django import forms

class DoctorAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Пароль")
    
    class Meta:
        model = Doctor
        fields = '__all__'

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    form = DoctorAdminForm
    list_display = ('name', 'specialization', 'experience', 'username')
    search_fields = ('name', 'specialization', 'username')
    list_filter = ('specialization',)
    
    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password'):
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', "order")
    search_fields = ('title', 'description')
    list_filter = ('order',)    

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'doctor', 'date', 'message', 'created_at')
    list_filter = ('doctor', 'date', 'created_at')
    search_fields = ('name', 'phone')
    date_hierarchy = 'date'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
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

# ДОБАВЛЯЕМ РЕГИСТРАЦИЮ МОДЕЛИ MedicalRecord
@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
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
        return f"{obj.appointment.name} ({obj.appointment.phone})"
    appointment_info.short_description = 'Пациент'
    
    def doctor_name(self, obj):
        return obj.doctor.name
    doctor_name.short_description = 'Врач'
    
    def created_at_short(self, obj):
        return obj.created_at.strftime("%d.%m.%Y %H:%M")
    created_at_short.short_description = 'Создано'
    
    def services_list(self, obj):
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

admin.site.site_header = "Администрирование клиники"