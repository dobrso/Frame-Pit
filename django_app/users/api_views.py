from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema

from .models import Profile
from .serializers import ProfileSerializer

@extend_schema(
    summary='Получить профиль',
    description='Возвращает профиль текущего пользователя. Требуется авторизация',
    tags=['Пользователи'],
)
class ProfileAPIView(generics.RetrieveAPIView):
    '''
    Эндпоинт для получения профиля текущего пользователя. Требуется авторизация
    '''

    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

