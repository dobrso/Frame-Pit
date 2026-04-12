from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField('Название', max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms', verbose_name='Создатель')

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return f'Комната {self.name}'