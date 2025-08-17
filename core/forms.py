import datetime
from django import forms
from .models import Doctor
from django.core.validators import RegexValidator

class AppointmentForm(forms.Form):
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