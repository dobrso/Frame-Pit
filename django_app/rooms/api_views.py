from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema

from .models import Room
from .serializers import SimpleRoomSerializer, RoomSerializer

@extend_schema(
    summary='Список комнат',
    description='Возвращает список всех доступных комнат',
    tags=['Комната'],
)
class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = SimpleRoomSerializer

@extend_schema(
    summary='Информация о комнате',
    description='Возвращает детальную информацию о комнате по его ID',
    tags=['Комната'],
)
class RoomDetailAPIView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_object(self):
        return Room.objects.get(id=self.kwargs['room_id'])