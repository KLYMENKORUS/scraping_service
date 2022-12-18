from django.db import models
from .utils import from_cyrilling_to_en


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название города', 
                            help_text='Не более 50 символов', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Название населенных пунктов'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrilling_to_en(str(self.name))
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name='Язык программирования', 
                            help_text='Не более 50 символов', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrilling_to_en(str(self.name))
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок вакансии')
    company = models.CharField(max_length=250, verbose_name='Кампания')
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, 
                                 verbose_name='Язык программирования')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f'{self.title} - {self.city}'


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self):
        return str(self.timestamp)

