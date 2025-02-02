from django.db import models
# Модель формы

# Поля с выпадающим списком
Activities = [
    ('1active', '1 Кружок'),
    ('2active', '2 Кружок'),
    ('3active', '3 Кружок'),
    ('4active', '4 Кружок'),
]
class Profile(models.Model):
    family = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    active = models.CharField(max_length=8, choices=Activities)
    clas = models.CharField(max_length=20)

    class Meta:
        ordering = ['id']
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f"{self.family} {self.name}, {self.active}"

