from django.shortcuts import render
from .models import Service, Doctor  # если используете модели

def home(request):
    services = Service.objects.all()
    doctors = Doctor.objects.all()
    
    context = {
    'services': services,
    'doctors': doctors,
    }
    return render(request, 'core\index.html', context)