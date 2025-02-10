from django.db import models
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
    family = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    active = models.CharField(max_length=50, choices=Activities)
    Class = models.CharField(max_length=20)

    class Meta:
        ordering = ['id']
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'

    def __str__(self):
        return f"{self.family} {self.name}, {self.active}"

