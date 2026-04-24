from django.db import models

class GalleryImage(models.Model):
    title = models.CharField('Название', max_length=200, blank=True)
    image = models.ImageField('Изображение', upload_to='gallery/')
    description = models.CharField('Описание', max_length=300, blank=True)
    order = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Изображение галереи'
        verbose_name_plural = 'Изображения галереи'

    def __str__(self):
        return self.title or f'Изображение {self.id}'