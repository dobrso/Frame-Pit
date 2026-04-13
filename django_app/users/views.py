from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterForm, ProfileForm
from .models import Profile

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(Profile, user=self.kwargs['user_id'])

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'users/profile_update.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(Profile, user=self.kwargs['user_id'])

    def get_success_url(self):
        return reverse_lazy('users:profile_detail', kwargs={'user_id': self.object.user.id})

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/profile_delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('main:home')

    def get_object(self):
        user = get_object_or_404(User, id=self.kwargs['user_id'])
        if user == self.request.user:
            return user
