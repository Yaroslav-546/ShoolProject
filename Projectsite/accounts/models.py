from django.contrib.auth.models import AbstractUser
from django.db import models

def user_avatar_path(instance, filename):
    return f'users/user_{instance.id}/{filename}'

class CustomUser(AbstractUser):
    patronymic = models.CharField('Отчество', max_length=150, blank=True)
    avatar = models.ImageField(
        'Аватар', 
        upload_to=user_avatar_path, 
        default='users/default_avatar.svg'
    )
    
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