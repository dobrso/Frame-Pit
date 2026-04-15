from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Tag(models.Model):
    name = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField('Название', max_length=100)
    image = models.ImageField('Изображение', blank=True, null=True, default='default/shell.jpg', upload_to='uploads/room/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_owners', verbose_name='Создатель')
    tags = models.ManyToManyField(Tag, blank=True, related_name='room_tags', verbose_name='Тэги')
    members = models.ManyToManyField(User, blank=True, related_name='room_members', verbose_name='Участники')

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return f'Комната {self.name}'

    def get_room_members_count(self):
        return self.members.count()

class Message(models.Model):
    text = models.TextField('Сообщение')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Комната')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'Сообщение от {self.user.username} в {self.room.name}'

class Poll(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='polls', verbose_name='Комната')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_polls', verbose_name='Создатель')
    question = models.CharField('Вопрос', max_length=300)
    is_active = models.BooleanField('Активно', default=True)
    expires_at = models.DateTimeField('Истекает', null=True, blank=True)

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return self.question

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options', verbose_name='Опрос')
    text = models.CharField('Вариант ответа', max_length=200)

    class Meta:
        verbose_name = 'Вариант опроса'
        verbose_name_plural = 'Варианты опросов'

    def __str__(self):
        return self.text

class PollVote(models.Model):
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='votes', verbose_name='Вариант')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poll_votes', verbose_name='Пользователь')
    voted_at = models.DateTimeField('Проголосовано', auto_now_add=True)

    class Meta:
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'
        unique_together = ['option', 'user']

    def __str__(self):
        return f'{self.user.username} - {self.option.text}'

@receiver(post_save, sender=Room)
def add_owner_to_members(sender, instance, created, **kwargs):
    if created:
        instance.members.add(instance.owner)