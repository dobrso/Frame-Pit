from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema

from .models import Room
from .serializers import SimpleRoomSerializer, RoomSerializer

@extend_schema(
    summary='Список комнат',
    description='Возвращает список всех доступных комнат. Поддерживается фильтрация по названию комнат',
    tags=['Комната'],
)
class RoomListAPIView(generics.ListAPIView):
    '''
    Эндпоинт для получения списка всех комнат
    Можно фильтровать названия комнат по имени
    '''

    queryset = Room.objects.all()
    serializer_class = SimpleRoomSerializer

    def get_queryset(self):
        queryset = Room.objects.all()

        search_query = self.request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

@extend_schema(
    summary='Информация о комнате',
    description='Возвращает детальную информацию о комнате по его ID',
    tags=['Комната'],
)
class RoomDetailAPIView(generics.RetrieveAPIView):
    '''
    Эндпоинт для получения информации о комнате
    '''

    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_object(self):
        return Room.objects.get(id=self.kwargs['room_id'])