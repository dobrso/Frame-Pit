from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import RegisterView, ProfileView, ProfileEditView, ProfileDeleteView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('profile/<int:user_id>/delete/', ProfileDeleteView.as_view(), name='profile_delete'),
]