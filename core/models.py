from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        app_label = 'core' 
    
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