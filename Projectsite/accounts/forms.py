from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import CustomUser
from .validators import validate_password_length
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext as _
from django.db.models import Q

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='Электронная почта',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control form-label', 'placeholder': 'Введите email'})
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        validators=[validate_password_length],
    )
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'last_name', 'first_name', 'patronymic')
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
    
    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email
    
    def save(self, commit=True, request=None):
        """Сохранение пользователя и отправка письма для верификации"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False  # Аккаунт неактивен до подтверждения email
        
        if commit:
            user.save()
            if request:
                user.send_verification_email(request)
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'patronymic', 'avatar', 'grade')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'patronymic': 'Отчество',
            'avatar': 'Аватар',
            'grade': 'Класс',
        }
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class PasswordResetRequestForm(forms.Form):
    """Форма запроса сброса пароля"""
    email = forms.EmailField(
        label='Электронная почта',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-label',
            'placeholder': 'Введите email, указанный при регистрации'
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            if not user.is_active:
                raise ValidationError('Аккаунт деактивирован. Обратитесь к администратору.')
        except CustomUser.DoesNotExist:
            raise ValidationError('Пользователь с таким email не найден.')
        return email

class CustomSetPasswordForm(SetPasswordForm):
    """Форма установки нового пароля"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Настройка полей
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control form-label',
            'placeholder': 'Введите новый пароль'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control form-label',
            'placeholder': 'Повторите новый пароль'
        })
        
        self.fields['new_password1'].label = 'Новый пароль'
        self.fields['new_password2'].label = 'Подтверждение пароля'
        
        self.fields['new_password1'].help_text = "Пароль должен содержать минимум 8 символов"

class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    """
    Форма входа, принимающая email или username
    Переопределяем поле username для понятного placeholder
    """
    username = forms.CharField(
        label='Логин или Email',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-label',
            'placeholder': 'Введите логин или email',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-label',
            'placeholder': 'Введите пароль'
        })
    )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            from django.contrib.auth import authenticate
            from .models import CustomUser
            
            # Пытаемся найти пользователя
            try:
                user = CustomUser.objects.get(
                    Q(username__iexact=username) | Q(email__iexact=username)
                )
                
                # Проверяем пароль
                if not user.check_password(password):
                    raise forms.ValidationError(
                        _("Неверный логин/email или пароль."),
                        code='invalid_login',
                    )
                
                # Проверяем активность
                self.confirm_login_allowed(user)
                self.user_cache = user
                
            except CustomUser.DoesNotExist:
                raise forms.ValidationError(
                    _("Неверный логин/email или пароль."),
                    code='invalid_login',
                )
        
        return self.cleaned_data

    def get_user(self):
        """Возвращает пользователя из кэша"""
        return self.user_cache