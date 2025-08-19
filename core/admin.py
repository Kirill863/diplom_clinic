from django.contrib import admin
from .models import Doctor, Service, Appointment, Testimonial


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'experience')
    search_fields = ('name', 'specialization')
    list_filter = ('specialization',)

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