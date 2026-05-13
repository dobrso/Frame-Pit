from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, RedirectView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from .forms import RoomForm
from .models import Room

class RoomsListView(ListView):
    '''
    Отображает страницу со списком всех комнат
    '''

    model = Room
    template_name = 'rooms/rooms_list.html'
    context_object_name = 'rooms'

class RoomCreateView(LoginRequiredMixin, CreateView):
    '''
    Отображает страницу с формой создания комнаты. Требуется авторизация
    '''

    model = Room
    form_class = RoomForm
    template_name = 'rooms/room_create.html'

    def get_initial(self):
        '''
        Получает черновик с данными о комнате, если они есть в сессии пользователя
        '''

        draft = self.request.session.get(f'room_draft_{self.request.user.id}')
        return draft or {}

    def form_invalid(self, form):
        '''
        Сохраняет данные о комнате в черновик, если форма невалидна
        '''

        draft_key = f'room_draft_{self.request.user.id}'
        draft_data = {
            'name': self.request.POST.get('name', ''),
            'tags': self.request.POST.getlist('tags'),
        }

        self.request.session[draft_key] = draft_data
        self.request.session.set_expiry(3600)

        return super().form_invalid(form)

    def form_valid(self, form):
        '''
        Удаляет черновик с данными о комнате, если форма валидна
        '''

        form.instance.owner = self.request.user

        draft_key = f'room_draft_{self.request.user.id}'
        if draft_key in self.request.session:
            del self.request.session[draft_key]

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('rooms:room_join', kwargs={'room_id': self.object.id})

class RoomDetailView(LoginRequiredMixin, DetailView):
    '''
    Отображает страницу с комнатой. Требуется авторизация
    '''

    model = Room
    template_name = 'rooms/room_detail.html'
    context_object_name = 'room'

    def get_object(self):
        return get_object_or_404(Room, id=self.kwargs['room_id'])

class RoomUpdateView(LoginRequiredMixin, UpdateView):
    '''
    Отображает страницу с формой для обновления данных комнаты. Требуется авторизация
    '''

    model = Room
    form_class = RoomForm
    template_name = 'rooms/room_update.html'
    context_object_name = 'room'

    def get_object(self):
        return get_object_or_404(Room, id=self.kwargs['room_id'])

    def get_success_url(self):
        return reverse_lazy('rooms:room_detail', kwargs={'room_id': self.kwargs['room_id']})

class RoomDeleteView(LoginRequiredMixin, DeleteView):
    '''
    Отображает страницу с формой удаления комнаты. Требуется авторизация
    '''

    model = Room
    template_name = 'rooms/room_delete.html'
    context_object_name = 'room'
    success_url = reverse_lazy('rooms:rooms_list')

    def get_object(self):
        room = get_object_or_404(Room, id=self.kwargs['room_id'])
        if room.owner == self.request.user:
            return room

class RoomJoinView(LoginRequiredMixin, RedirectView):
    '''
    Перенаправляет пользователя на страницу с комнатой, тем самым добавляет его в список участников. Требуется авторизация
    '''

    def get_redirect_url(self, *args, **kwargs):
        room = get_object_or_404(Room, id=self.kwargs['room_id'])
        room.members.add(self.request.user)

        return reverse_lazy('rooms:room_detail', kwargs={'room_id': self.kwargs['room_id']})

class RoomLeaveView(LoginRequiredMixin, RedirectView):
    '''
    Перенаправляет пользователя со страницы комнаты, тем самым удаляет его из списка участников. Требуется авторизация
    '''

    def get_redirect_url(self, *args, **kwargs):
        room = get_object_or_404(Room, id=self.kwargs['room_id'])
        room.members.remove(self.request.user)

        if room.members.count() == 0:
            room.delete()

        return reverse_lazy('rooms:rooms_list')