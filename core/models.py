"""
Модели Django для системы управления клиникой.

Модуль содержит определения моделей данных для основных сущностей системы:
пациентов, врачей, услуг, записей на прием, отзывов и медицинских карт.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.hashers import make_password, check_password


class Patient(models.Model):
    """
    Модель пациента клиники.
    
    Хранит основную информацию о пациентах: имя, контактные данные,
    дату рождения и дополнительные заметки.
    
    Attributes:
        name (CharField): Полное имя пациента
        phone (CharField): Контактный телефон
        birth_date (DateField): Дата рождения (опционально)
        notes (TextField): Дополнительные медицинские заметки
    """
    
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
    """
    Модель медицинской услуги.
    
    Описывает услуги, предоставляемые клиникой, с названием,
    описанием и порядком отображения.
    
    Attributes:
        title (CharField): Название услуги
        description (TextField): Подробное описание услуги
        order (PositiveIntegerField): Порядок сортировки для отображения
    """
    
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
    """
    Модель врача клиники.
    
    Содержит информацию о медицинских специалистах: ФИО, специализацию,
    опыт работы, описание и учетные данные для входа в систему.
    
    Attributes:
        name (CharField): Полное имя врача
        specialization (CharField): Медицинская специализация
        experience (IntegerField): Стаж работы в годах
        description (TextField): Подробное описание квалификации
        username (CharField): Уникальный логин для входа
        password (CharField): Хешированный пароль
    """
    
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
        """Хеширование и установка пароля врача."""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Проверка соответствия пароля."""
        return check_password(raw_password, self.password)


class Appointment(models.Model):
    """
    Модель записи на прием к врачу.
    
    Содержит информацию о назначенных приемах: пациент, врач,
    дата и время, статус обработки записи.
    
    Attributes:
        STATUS_CHOICES (list): Варианты статусов записи
        name (CharField): Имя пациента
        phone (CharField): Контактный телефон
        doctor (ForeignKey): Ссылка на врача
        date (DateField): Дата приема
        message (TextField): Дополнительное сообщение
        created_at (DateTimeField): Дата создания записи
        patient (ForeignKey): Ссылка на модель пациента (опционально)
        status (CharField): Текущий статус записи
    """
    
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждена'),
        ('cancelled', 'Отменена'),
        ('completed', 'Завершена'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Имя пациента')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Врач')
    date = models.DateField(verbose_name='Дата приема')
    message = models.TextField(blank=True, verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, verbose_name='Пациент', null=True, blank=True)
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name='Статус записи'
    )

    class Meta:
        verbose_name = 'Запись на прием'
        verbose_name_plural = 'Записи на прием'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.doctor} ({self.date})'


class Testimonial(models.Model):
    """
    Модель отзыва пациента о клинике.
    
    Хранит отзывы пациентов с оценкой качества обслуживания
    и информацией о враче. Требует модерации перед публикацией.
    
    Attributes:
        RATING_CHOICES (list): Варианты оценок
        name (CharField): Имя пациента
        doctor (ForeignKey): Врач, к которому относится отзыв
        message (TextField): Текст отзыва
        rating (CharField): Оценка обслуживания
        created_at (DateTimeField): Дата создания отзыва
        is_approved (BooleanField): Флаг одобрения модератором
    """
    
    RATING_CHOICES = [
        ('good', 'Хорошо'),
        ('bad', 'Плохо'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Имя пациента")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Врач')
    message = models.TextField(verbose_name="Текст отзыв")
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
        """Возвращает CSS-класс для отображения оценки."""
        return 'success' if self.rating == 'good' else 'danger'
    
    def get_rating_icon(self):
        """Возвращает иконку FontAwesome для оценки."""
        return 'fa-smile' if self.rating == 'good' else 'fa-frown'


class MedicalRecord(models.Model):
    """
    Модель медицинской карты пациента.
    
    Содержит полную медицинскую информацию о приеме: диагноз,
    назначенное лечение, оказанные услуги и рекомендации.
    
    Attributes:
        appointment (ForeignKey): Связанная запись на прием
        doctor (ForeignKey): Лечащий врач
        services (ManyToManyField): Оказанные медицинские услуги
        diagnosis (TextField): Поставленный диагноз
        treatment (TextField): Назначенное лечение
        recommendations (TextField): Рекомендации пациенту
        created_at (DateTimeField): Дата создания записи
        patient (ForeignKey): Ссылка на пациента (опционально)
    """
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, verbose_name='Запись на прием')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Врач')
    services = models.ManyToManyField(Service, verbose_name='Услуги')
    diagnosis = models.TextField(verbose_name='Диагноз')
    treatment = models.TextField(verbose_name='Лечение')
    recommendations = models.TextField(blank=True, verbose_name='Рекомендации')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, verbose_name='Пациент', null=True, blank=True)

    class Meta:
        verbose_name = 'Медицинская запись'
        verbose_name_plural = 'Медицинские записи'
    
    def __str__(self):
        return f"Запись от {self.created_at.strftime('%d.%m.%Y')} - {self.appointment.name}"