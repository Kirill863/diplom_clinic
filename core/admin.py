from django.contrib import admin
from .models import Doctor, Service, Appointment

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

admin.site.site_header = "Администрирование клиники"