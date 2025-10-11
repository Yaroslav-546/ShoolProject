from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .validators import validate_password_length

class CustomUserCreationForm(UserCreationForm):
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        validators=[validate_password_length],
    )
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'last_name', 'first_name', 'patronymic')
        labels = {
            'username': 'Логин',
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'patronymic': 'Отчество',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].help_text = None

        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'

        self.fields['username'].widget.attrs['placeholder'] = 'Введите логин'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['patronymic'].widget.attrs['placeholder'] = 'Введите отчество'

        self.fields['last_name'].required = True
        self.fields['first_name'].required = True
        self.fields['patronymic'].required = True

        self.fields['password1'].help_text = "Пароль должен содержать минимум 8 символов"
        self.fields['username'].help_text = "Только буквы, цифры и символы @/./+/-/_"

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-label'})

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'patronymic', 'avatar')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'patronymic': 'Отчество',
            'avatar': 'Аватар',
        }
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
        }