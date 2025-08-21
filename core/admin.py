from django.contrib import admin
from .models import Doctor, Service, Appointment, Testimonial
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


admin.site.site_header = "Администрирование клиники"