from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service, Doctor, Testimonial, Appointment, MedicalRecord
from .forms import AppointmentForm, TestimonialForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Doctor, Appointment
from .forms import MedicalRecordForm

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



def staff_login(request):
    """Страница входа для персонала"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None and user.is_staff:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('admin:index')  # Перенаправляем в админку
            else:
                messages.error(request, 'Неверные учетные данные или недостаточно прав')
        else:
            messages.error(request, 'Пожалуйста, проверьте введенные данные')
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/staff_login.html', {'form': form})


def doctor_login(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'doctor':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            try:
                doctor = Doctor.objects.get(username=username)
                if doctor.check_password(password):
                    request.session['doctor_id'] = doctor.id
                    request.session['doctor_name'] = doctor.name
                    return redirect('doctor_dashboard')
                else:
                    messages.error(request, 'Неверный пароль')
            except Doctor.DoesNotExist:
                messages.error(request, 'Врач с таким логином не найден')
            
            # Сохраняем в сессии тип формы для отображения сообщений
            request.session['form_type'] = 'doctor'
            return redirect('core/staff_login')
    
    return redirect('core/staff_login')

@login_required
def doctor_dashboard(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')
    
    doctor = get_object_or_404(Doctor, id=doctor_id)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-created_at')
    
    return render(request, 'core/doctor_dashboard.html', {
        'doctor': doctor,
        'appointments': appointments
    })

def doctor_logout(request):
    if 'doctor_id' in request.session:
        del request.session['doctor_id']
    if 'doctor_name' in request.session:
        del request.session['doctor_name']
    return redirect('core/staff_login')



@login_required
def patient_card(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    medical_records = MedicalRecord.objects.filter(appointment=appointment)
        
    patient_history = Appointment.objects.filter(
        phone=appointment.phone
    ).order_by('-date')
    
    context = {
        'appointment': appointment,
        'medical_records': medical_records,  # Добавьте это в контекст
        'patient_history': patient_history,
        'doctor': appointment.doctor
    }
    
    # Исправьте путь к шаблону
    return render(request, 'core/patient_card.html', context)

@login_required
def create_medical_record(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.appointment = appointment
            medical_record.doctor = appointment.doctor
            medical_record.save()
            form.save_m2m()
            
            # Переадресация на список медицинских записей
            return redirect('core/medical_records_list', appointment_id=appointment.id)
    else:
        form = MedicalRecordForm()
    
    return render(request, 'core/create_medical_record.html', {
        'form': form,
        'appointment': appointment
    })


@login_required
def medical_records_list(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    medical_records = MedicalRecord.objects.filter(appointment=appointment).order_by('-created_at')
    
    context = {
        'appointment': appointment,
        'medical_records': medical_records
    }
    return render(request, 'core/medical_records_list.html', context)