from django import forms

from .models import Room, Tag

class RoomForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False, label='Тэги')

    class Meta:
        model = Room
        fields = ['name', 'image', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        room_id = self.instance.id if self.instance else None
        if Room.objects.filter(name=name).exclude(id=room_id).exists():
            raise forms.ValidationError('Комната с таким названием уже существует!')
        return name