from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError

class News(models.Model):
    title = models.CharField('Название',max_length=200)
    body = models.TextField('Содержание')
    date = models.DateTimeField('Дата',auto_now_add=True)
    image = models.ImageField('Изображение',upload_to='images/', blank=False)

    class Meta:
        ordering = ['-date',]
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def clean(self):
        if len(self.title) > 200:
            raise ValidationError({'title': 'Заголовок не может превышать 200 символов.'})