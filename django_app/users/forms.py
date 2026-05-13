from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm

from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Кастомные атрибуты для полей
        self.fields['username'].widget.attrs.update({
            'class': 'roulette-input',
            'autofocus': 'autofocus'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'roulette-input',
            'autocomplete': 'email'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'roulette-input',
            'autocomplete': 'new-password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'roulette-input',
            'autocomplete': 'new-password'
        })

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с такой почтой уже существует!")
        return email

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'roulette-input',
            'autocomplete': 'username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'roulette-input',
            'autocomplete': 'current-password'
        })


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'roulette-textarea',
                'rows': 5,
                'placeholder': 'ВВЕДИТЕ ИНФОРМАЦИЮ О СЕБЕ...\nВАШИ НАВЫКИ, ПРЕДПОЧТЕНИЯ, ОПЫТ...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'roulette-file-input',
                'accept': 'image/*'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Кастомные атрибуты для полей
        self.fields['description'].widget.attrs.update({
            'class': 'roulette-textarea',
        })

        self.fields['image'].widget.attrs.update({
            'class': 'roulette-file-input',
        })

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Кастомные атрибуты для поля email
        self.fields['email'].widget.attrs.update({
            'class': 'roulette-input',
            'autocomplete': 'email',
            'autofocus': 'autofocus'
        })

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Заменяем Bootstrap классы на кастомные для Buckshot стиля
        self.fields['new_password1'].widget.attrs.update({
            'class': 'roulette-input',
            'autocomplete': 'new-password',
            'autofocus': 'autofocus'
        })

        self.fields['new_password2'].widget.attrs.update({
            'class': 'roulette-input',
            'autocomplete': 'new-password'
        })