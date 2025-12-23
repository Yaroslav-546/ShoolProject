from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from .validators import validate_grade_contains
from django.utils import timezone
from datetime import timedelta
import secrets
from django.conf import settings

def user_avatar_path(instance, filename):
    return f'users/user_{instance.id}/{filename}'

class UpperField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(UpperField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value == None:
            return value
        return str(value).upper()

class CustomUser(AbstractUser):
    patronymic = models.CharField('Отчество', max_length=150, blank=True)
    avatar = models.ImageField(
        'Аватар', 
        upload_to=user_avatar_path, 
        default='users/default_avatar.svg'
    )
    grade = UpperField('Класс', max_length=3, blank=True, null=True, validators=[validate_grade_contains])
    email = models.EmailField('Электронная почта', unique=True, blank=False)
    email_verified = models.BooleanField('Почта подтверждена', default=False)
    email_verification_token = models.CharField('Токен подтверждения', max_length=64, blank=True, null=True)

    reset_password_token = models.CharField('Токен сброса пароля', max_length=64, blank=True, null=True)
    reset_password_expires = models.DateTimeField('Срок действия токена', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    def get_full_name(self):
        full_name = f"{self.last_name} {self.first_name}"

        if self.patronymic:
            full_name += f" {self.patronymic}"
            
        return full_name.strip()
    
    def generate_password_reset_token(self):
        """Генерация токена для сброса пароля"""
        self.reset_password_token = secrets.token_urlsafe(32)
        self.reset_password_expires = timezone.now() + timedelta(hours=24)  # Токен на 24 часа
        self.save()
        return self.reset_password_token
    
    def send_password_reset_email(self, request):
        """Отправка письма для сброса пароля"""
        from django.urls import reverse
        
        token = self.generate_password_reset_token()
        reset_url = request.build_absolute_uri(
            reverse('password-reset-confirm', kwargs={'token': token})
        )
        
        subject = 'Сброс пароля на сайте'
        message = f'''
        Здравствуйте, {self.first_name}!
        
        Вы запросили сброс пароля для вашего аккаунта.
        
        Для установки нового пароля перейдите по ссылке:
        {reset_url}
        
        Ссылка действительна в течение 24 часов.
        
        Если вы не запрашивали сброс пароля, проигнорируйте это письмо.
        '''
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
        )
    
    def is_password_reset_token_valid(self):
        """Проверка валидности токена сброса пароля"""
        if not self.reset_password_token or not self.reset_password_expires:
            return False
        return timezone.now() <= self.reset_password_expires
    
    def clear_password_reset_token(self):
        """Очистка токена после использования"""
        self.reset_password_token = None
        self.reset_password_expires = None
        self.save()
    
    def generate_verification_token(self):
        """Генерация токена для верификации почты"""
        import secrets
        self.email_verification_token = secrets.token_urlsafe(32)
        self.save()
        return self.email_verification_token
    
    def send_verification_email(self, request):
        """Отправка письма с ссылкой для подтверждения"""
        from django.urls import reverse
        
        token = self.generate_verification_token()
        verification_url = request.build_absolute_uri(
            reverse('verify-email', kwargs={'token': token})
        )
        
        subject = 'Подтверждение электронной почты'
        message = f'''
        Здравствуйте, {self.first_name}!
        
        Для завершения регистрации подтвердите ваш адрес электронной почты, перейдя по ссылке:
        {verification_url}
        
        Если вы не регистрировались на нашем сайте, проигнорируйте это письмо.
        '''
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER, 
            [self.email],
            fail_silently=False,
        )