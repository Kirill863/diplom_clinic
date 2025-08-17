from django.db import models

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
    
    class Meta:
        app_label = 'core'
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
    
    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя пациента')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Врач')
    date = models.DateField(verbose_name='Дата приема')
    message = models.TextField(blank=True, verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')

    class Meta:
        verbose_name = 'Запись на прием'
        verbose_name_plural = 'Записи на прием'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.doctor} ({self.date})'