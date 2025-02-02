from django import forms
from .models import Profile

# Форма для записи на кружок
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        labels = {
            'family': 'Фамилия',
            'name': 'Имя',
            'active': 'Кружок',
            'clas': 'Класс',
        }

    # Скопировали из инета, присваевает полю input класс бутстрап (т.е стилизация)
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-label'})