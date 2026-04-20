from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Feedback(models.Model):
    """
    Модель обратной связи: сохраняет все сообщения от пользователей
    """
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('read', 'Прочитано'),
        ('replied', 'Ответ дан'),
        ('closed', 'Закрыто'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Email')
    subject = models.CharField('Тема', max_length=200)
    message = models.TextField('Сообщение')
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    admin_reply = models.TextField('Ответ администратора', blank=True, null=True)
    replied_at = models.DateTimeField('Дата ответа', blank=True, null=True)

    class Meta:
        verbose_name = 'Сообщение обратной связи'
        verbose_name_plural = 'Сообщения обратной связи'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.subject[:50]}'