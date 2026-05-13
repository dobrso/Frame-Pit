from django import forms

from .models import Room, Tag


class RoomForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Тэги'
    )

    class Meta:
        model = Room
        fields = ['name', 'image', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'roulette-input',
                'autofocus': 'autofocus'
            }),
            'image': forms.FileInput(attrs={
                'class': 'roulette-file-input',
                'accept': 'image/*'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Кастомные атрибуты для полей
        self.fields['name'].widget.attrs.update({
            'class': 'roulette-input',
        })

        self.fields['image'].widget.attrs.update({
            'class': 'roulette-file-input',
        })

        self.fields['image'].help_text = 'Поддерживаются JPG, PNG, GIF. Максимум 5MB.'
        self.fields['tags'].help_text = 'Выберите теги для вашей комнаты'

        # Настройка стилей для виджета CheckboxSelectMultiple
        self.fields['tags'].widget.attrs.update({
            'class': 'roulette-checkbox-group'
        })

    def clean_name(self):
        name = self.cleaned_data['name']
        room_id = self.instance.id if self.instance else None
        if Room.objects.filter(name=name).exclude(id=room_id).exists():
            raise forms.ValidationError('КОМНАТА С ТАКИМ НАЗВАНИЕМ УЖЕ СУЩЕСТВУЕТ!')
        return name