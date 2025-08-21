from django.db import models
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.hashers import make_password, check_password


class Patient(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя пациента')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    notes = models.TextField(blank=True, verbose_name='Заметки')
    
    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'
    
    def __str__(self):
        return self.name

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = 'core' 
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        
    def __str__(self):
        return self.title

class Doctor(models.Model):
    name = models.CharField(max_length=100, verbose_name='ФИО врача')
    specialization = models.CharField(max_length=100, verbose_name='Специализация')
    experience = models.IntegerField(verbose_name='Стаж работы (лет)', default=0, blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    username = models.CharField(max_length=50, unique=True, verbose_name='Логин', blank=True, null=True)
    password = models.CharField(max_length=128, verbose_name='Пароль', blank=True, null=True)

    class Meta:
        app_label = 'core'
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
    
    def __str__(self):
        return self.name
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
class Appointment(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя пациента')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Врач')
    date = models.DateField(verbose_name='Дата приема')
    message = models.TextField(blank=True, verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, verbose_name='Пациент', null=True, blank=True)

    class Meta:
        verbose_name = 'Запись на прием'
        verbose_name_plural = 'Записи на прием'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.doctor} ({self.date})'



class Testimonial(models.Model):
    RATING_CHOICES = [
        ('good', 'Хорошо'),
        ('bad', 'Плохо'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Имя пациента")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Врач')
    message = models.TextField(verbose_name="Текст отзыва")
    rating = models.CharField(
        max_length=10,
        choices=RATING_CHOICES,
        default='good',
        verbose_name="Оценка"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_approved = models.BooleanField(default=False, verbose_name="Одобрено")
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Отзыв от {self.name}"
    
    def get_rating_display_class(self):
        return 'success' if self.rating == 'good' else 'danger'
    
    def get_rating_icon(self):
        return 'fa-smile' if self.rating == 'good' else 'fa-frown'
    
