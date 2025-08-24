from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service, Doctor, Testimonial, Appointment, MedicalRecord
from .forms import AppointmentForm, TestimonialForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import MedicalRecordForm
from django.utils import timezone

def home(request):
    """Главная страница с услугами, врачами и отзывами"""
    # Получаем услуги
    services = Service.objects.all()
    testimonials = Testimonial.objects.all()
    doctors = Doctor.objects.all()
    
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
            # Проверяем, нет ли дублирующей записи с Q-запросом
            existing_appointment = Appointment.objects.filter(
                Q(phone=form.cleaned_data['phone']) &
                Q(doctor=form.cleaned_data['doctor']) &
                Q(date=form.cleaned_data['date'])
            ).exists()
            
            if existing_appointment:
                messages.warning(request, 'У вас уже есть запись на это время к данному врачу.')
                return render(request, 'core/appointment.html', {'form': form})
            
            # Сохраняем форму
            appointment = form.save()
            messages.success(request, 'Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.')
            return redirect('appointment_success')
    else:
        form = AppointmentForm()
    
    return render(request, 'core/appointment.html', {'form': form})

def appointment_success(request):
    """Страница успешной записи"""
    return render(request, 'core/appointment_success.html')

def add_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            # Проверяем, не оставлял ли пользователь уже отзыв для этого врача с таким же сообщением
            name = form.cleaned_data['name']
            doctor = form.cleaned_data['doctor']
            message = form.cleaned_data['message']
            
            recent_testimonial = Testimonial.objects.filter(
                name=name,
                doctor=doctor,
                message=message
            ).exists()
            
            if recent_testimonial:
                messages.error(request, 'Вы уже оставляли отзыв для этого врача с таким же сообщением.')
                return redirect('testimonials')
            
            # Сохраняем форму (создает и сохраняет объект)
            testimonial = form.save(commit=False)
            testimonial.is_approved = False  # если нужно модерацию
            testimonial.save()
            
            messages.success(request, 'Ваш отзыв успешно отправлен и ожидает модерации.')
            return redirect('home')
    else:
        form = TestimonialForm()
    
    return render(request, 'core/add_testimonial.html', {'form': form})


def all_testimonials(request):
    """Страница со всеми отзывами с фильтрацией"""
    rating_filter = request.GET.get('rating')
    search_query = request.GET.get('search', '')
    
    testimonials = Testimonial.objects.filter(is_approved=True)
    
    # Применяем фильтрацию без Q-запросов
    if rating_filter:
        testimonials = testimonials.filter(rating=rating_filter)
    
    if search_query:
        testimonials = testimonials.filter(
            author_name__icontains=search_query
        ) | testimonials.filter(
            content__icontains=search_query
        )
    
    testimonials = testimonials.order_by('-created_at')
    
    context = {
        'testimonials': testimonials,
        'rating_filter': rating_filter,
        'search_query': search_query,
    }
    return render(request, 'core/index.html', context)

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
                return redirect('admin:index')
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
                # Убираем фильтр по is_active, так как этого поля нет
                doctor = Doctor.objects.filter(username=username).first()
                
                if doctor and doctor.check_password(password):
                    request.session['doctor_id'] = doctor.id
                    request.session['doctor_name'] = doctor.name
                    return redirect('doctor_dashboard')
                else:
                    messages.error(request, 'Неверный пароль')
            except Doctor.DoesNotExist:
                messages.error(request, 'Врач с таким логином не найден')
            
            request.session['form_type'] = 'doctor'
            return redirect('staff_login')
    
    return redirect('staff_login')

@login_required
def doctor_dashboard(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')
    
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    # Добавляем фильтрацию через Q-запросы
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')
    
    base_query = Appointment.objects.filter(doctor=doctor)
    
    # Фильтрация по статусу с Q
    if status_filter == 'confirmed':
        base_query = base_query.filter(status='confirmed')
    elif status_filter == 'pending':
        base_query = base_query.filter(status='pending')
    elif status_filter == 'cancelled':
        base_query = base_query.filter(status='cancelled')
    elif status_filter == 'completed':
        base_query = base_query.filter(status='completed')
    # Добавьте другие статусы, если они есть в вашей модели
    
    # Поиск с Q-запросом
    if search_query:
        base_query = base_query.filter(
            Q(name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(message__icontains=search_query)
        )
    
    appointments = base_query.order_by('-date', '-created_at')
    
    return render(request, 'core/doctor_dashboard.html', {
        'doctor': doctor,
        'appointments': appointments,
        'status_filter': status_filter,
        'search_query': search_query
    })

def doctor_logout(request):
    if 'doctor_id' in request.session:
        del request.session['doctor_id']
    if 'doctor_name' in request.session:
        del request.session['doctor_name']
    return redirect('staff_login')

@login_required
def patient_card(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Получаем медицинские записи
    medical_records = MedicalRecord.objects.filter(appointment=appointment)
    
    # История пациента
    patient_history = Appointment.objects.filter(
        Q(phone=appointment.phone)
    ).order_by('-date')
    
    context = {
        'appointment': appointment,
        'medical_records': medical_records,
        'patient_history': patient_history,
        'doctor': appointment.doctor
    }
    
    return render(request, 'core/patient_card.html', context)

@login_required
def create_medical_record(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            # Проверяем, нет ли похожей записи с Q-запросом
            similar_record = MedicalRecord.objects.filter(
                Q(appointment=appointment) &
                Q(diagnosis__icontains=form.cleaned_data['diagnosis']) &
                Q(created_at__date=timezone.now().date())
            ).exists()
            
            if similar_record:
                messages.warning(request, 'Похожая медицинская запись уже существует сегодня.')
                return render(request, 'core/create_medical_record.html', {
                    'form': form,
                    'appointment': appointment
                })
            
            medical_record = form.save(commit=False)
            medical_record.appointment = appointment
            medical_record.doctor = appointment.doctor
            medical_record.save()
            form.save_m2m()
            
            return redirect('patient_card', appointment_id=appointment.id)
    else:
        form = MedicalRecordForm()
    
    return render(request, 'core/create_medical_record.html', {
        'form': form,
        'appointment': appointment
    })

@login_required
def medical_records_list(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Фильтрация медицинских записей
    medical_records = MedicalRecord.objects.filter(appointment=appointment)
    
    medical_records = medical_records.order_by('-created_at')
    
    context = {
        'appointment': appointment,
        'medical_records': medical_records,
    }
    return render(request, 'core/medical_records_list.html', context)