
"""
Формы Django для приложения Core системы управления клиникой.

Модуль содержит классы форм для обработки данных записей на прием,
отзывов пациентов и медицинских карт. Формы обеспечивают валидацию
данных, настройку виджетов и пользовательский интерфейс.
"""

import datetime
from django import forms
from .models import Appointment, Doctor, MedicalRecord, Testimonial
from django.core.validators import RegexValidator


class AppointmentForm(forms.ModelForm):
    """
    Форма для записи пациента на прием к врачу.
    
    Обеспечивает валидацию контактных данных, выбор специалиста
    и даты приема. Включает кастомные виджеты для улучшения UX.
    
    Attributes:
        name (CharField): Имя пациента с валидацией длины
        phone (CharField): Номер телефона с regex-валидацией
        doctor (ModelChoiceField): Выбор врача из доступных специалистов
        date (DateField): Дата приема с ограничением на прошедшие даты
        message (CharField): Дополнительное сообщение (необязательное)
    """
    
    name = forms.CharField(
        label='Ваше имя',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя',
            'required': 'required'
        })
    )
    
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр."
        )],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Телефон',
            'required': 'required'
        })
    )
    
    doctor = forms.ModelChoiceField(
        label='Специалист',
        queryset=Doctor.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label='Выберите специалиста'
    )
    
    date = forms.DateField(
        label='Дата приема',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': datetime.date.today().strftime('%Y-%m-%d')
        }),
        input_formats=['%Y-%m-%d']
    )
    
    message = forms.CharField(
        label='Сообщение',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Сообщение (необязательно)'
        })
    )
    
    class Meta:
        """Метаданные формы для связи с моделью Appointment."""
        model = Appointment
        fields = ['name', 'phone', 'doctor', 'date', 'message']


class TestimonialForm(forms.ModelForm):
    """
    Форма для добавления отзывов пациентами о работе клиники и врачей.
    
    Включает выбор врача, текстовое описание и рейтингую систему.
    Настраивает виджеты для улучшения пользовательского опыта.
    
    Attributes:
        name (CharField): Имя пациента, оставившего отзыв
        doctor (ModelChoiceField): Врач, к которому относится отзыв
        message (CharField): Текст отзыва
        rating (ChoiceField): Оценка от 1 до 5 в виде radio-кнопок
    """
    
    class Meta:
        """Метаданные формы для связи с моделью Testimonial."""
        model = Testimonial
        fields = ['name', 'doctor', 'message', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя *'
            }),
            'doctor': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Выберите врача'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Поделитесь вашими впечатлениями о клинике *'
            }),
            'rating': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        """
        Инициализация формы с дополнительными настройками.
        
        Убирает пустую метку для поля рейтинга, обеспечивая
        обязательный выбор оценки.
        """
        super().__init__(*args, **kwargs)
        self.fields['rating'].empty_label = None


class MedicalRecordForm(forms.ModelForm):
    """
    Форма для создания и редактирования медицинских карт пациентов.
    
    Используется врачами для внесения информации о диагнозе,
    лечении, оказанных услугах и рекомендациях.
    
    Attributes:
        services (ModelMultipleChoiceField): Выбор оказанных медицинских услуг
        diagnosis (CharField): Поставленный диагноз
        treatment (CharField): Назначенное лечение
        recommendations (CharField): Рекомендации пациенту
    """
    
    class Meta:
        """Метаданные формы для связи с моделью MedicalRecord."""
        model = MedicalRecord
        fields = ['services', 'diagnosis', 'treatment', 'recommendations']
        widgets = {
            'services': forms.CheckboxSelectMultiple(),
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'treatment': forms.Textarea(attrs={'rows': 3}),
            'recommendations': forms.Textarea(attrs={'rows': 3}),
        }
