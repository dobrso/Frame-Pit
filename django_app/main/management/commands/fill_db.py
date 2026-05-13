from random import choice

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from users.models import Profile
from rooms.models import Tag, Room

class Command(BaseCommand):
    def handle(self, *args, **options):
        users = self._create_users()
        tags = self._create_tags()
        self._create_rooms(users, tags)

        self.stdout.write('БД заполнена данными')

    def _create_users(self):
        User = get_user_model()
        users = []

        if not User.objects.filter(username='framepitadmin').exists():
            admin = User.objects.create_superuser(username='framepitadmin', email='framepit@example.com', password='framepitadmin')
            Profile.objects.create(user=admin)
            self.stdout.write('Создан админ')

        for i in range(5):
            name = f'pituser_{i+1}'
            user, created = User.objects.get_or_create(username=name, defaults={'email': f'{name}@example.com'})

            if created:
                user.set_password(name)
                user.save()
                Profile.objects.create(user=user)
                self.stdout.write(f'Создан пользователь {name}')
            users.append(user)

        return users

    def _create_tags(self):
        names = ['Фильмы', 'Игры', 'Мультики']
        tags = []

        for name in names:
            Tag.objects.get_or_create(name=name)
            tags.append(name)

        self.stdout.write('Созданы теги')
        return tags

    def _create_rooms(self, users, tags):
        for i in range(10):
            user = choice(users)
            name = f'Комната {user.username}'

            room, _ = Room.objects.get_or_create(name=name, owner=user)
            room.tags.add(choice(tags))
            room.members.add(user)

        self.stdout.write('Созданы комнаты')