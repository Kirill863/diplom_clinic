from django.shortcuts import render, redirect
from core.models import Service, Doctor  # если используете модели
from .forms import AppointmentForm
from django.contrib import messages
from .models import Appointment

def home(request):
    services = Service.objects.all()
    doctors = Doctor.objects.all()
    
    context = {
    'services': services,
    'doctors': doctors,
    }
    return render(request, 'core\index.html', context)




def appointment_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = Appointment(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                doctor=form.cleaned_data['doctor'],
                date=form.cleaned_data['date'],
                message=form.cleaned_data['message']
            )
            appointment.save()
            messages.success(request, 'Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.')
            return redirect('appointment_success')
    else:
        form = AppointmentForm()
    
    return render(request, 'core/appointment.html', {'form': form})

def appointment_success(request):
    return render(request, 'core/appointment_success.html')