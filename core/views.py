from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service, Doctor, Testimonial, Appointment
from .forms import AppointmentForm, TestimonialForm

def home(request):
    """Главная страница с услугами, врачами и отзывами"""
    # Получаем услуги
    services = Service.objects.all()
    
    # Получаем врачей
    doctors = Doctor.objects.all()
    
    # Получаем одобренные отзывы
    testimonials = Testimonial.objects.filter(
        is_approved=True
    ).order_by('-created_at')[:6]
    
    context = {
        'services': services,
        'doctors': doctors,
        'testimonials': testimonials,
    }
    return render(request, 'core/index.html', context)

def appointment_view(request):
    """Страница записи на прием"""
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
    """Страница успешной записи"""
    return render(request, 'core/appointment_success.html')

def add_testimonial(request):
    """Отдельная страница для добавления отзыва"""
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.is_approved = False  # Требует модерации
            testimonial.save()
            
            messages.success(
                request, 
                'Спасибо за ваш отзыв! Он появится на сайте после проверки администратором.'
            )
            return redirect('add_testimonial')  # Исправлено: убрал 'core/'
    else:
        form = TestimonialForm()
    
    context = {
        'form': form,
    }
    return render(request, 'core/add_testimonial.html', context)

def all_testimonials(request):
    """Страница со всеми отзывами"""
    testimonials = Testimonial.objects.filter(is_approved=True).order_by('-created_at')
    
    context = {
        'testimonials': testimonials,
    }
    return render(request, 'core/all_testimonials.html', context)