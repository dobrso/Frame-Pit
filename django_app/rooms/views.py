from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from .forms import RoomForm
from .models import Room

class RoomsListView(ListView):
    model = Room
    template_name = 'rooms/rooms_list.html'
    context_object_name = 'rooms'

class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'rooms/room_create.html'
    success_url = reverse_lazy('rooms:rooms_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Room
    template_name = 'rooms/room_detail.html'
    context_object_name = 'room'

    def get_object(self):
        return get_object_or_404(Room, id=self.kwargs['room_id'])

class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'rooms/room_update.html'
    context_object_name = 'room'

    def get_object(self):
        return get_object_or_404(Room, id=self.kwargs['room_id'])

    def get_success_url(self):
        return reverse_lazy('rooms:room_detail', kwargs={'room_id': self.kwargs['room_id']})

class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'rooms/room_delete.html'
    context_object_name = 'room'
    success_url = reverse_lazy('rooms:rooms_list')

    def get_object(self):
        room = get_object_or_404(Room, id=self.kwargs['room_id'])
        if room.owner == self.request.user:
            return room