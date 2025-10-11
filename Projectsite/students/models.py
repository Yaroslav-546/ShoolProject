from django.db import models
from django.conf import settings
# Модель формы

# Поля с выпадающим списком
Activities = [
    ('Робототехника, старшая группа', 'Робототехника, старшая группа'),
    ('Геоинформатика', 'Геоинформатика'),
    ('Робототехника, младшая группа', 'Робототехника, младшая группа'),
    ('Промышленный дизайн', 'Промышленный дизайн'),
    ('Виртуальная и дополненная реальность', 'Виртуальная и дополненная реальность'),
    ('Программирование', 'Программирование'),
    ('Фото и видиосъёмка', 'Фото и видиосъёмка'),
    ('Шахматы', 'Шахматы'),
    ('ОБЖ', 'ОБЖ'),
]
class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    family = models.CharField(max_length=50, verbose_name='Фамилия')
    name = models.CharField(max_length=50, verbose_name='Имя')
    active = models.CharField(max_length=50, choices=Activities, verbose_name='Кружок')
    Class = models.CharField(max_length=3, verbose_name='Класс')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата записи')


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
        unique_together = ['user', 'active']

    def __str__(self):
        return f"{self.family} {self.name}, {self.active}"

