from django.db import models
from django.urls import reverse

#Модель пост- новости
class News(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/')

    class Meta:
        ordering = ['-date',]
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    #Возвращает название в БД в админ панели
    def __str__(self):
        return self.title

    # Для показа новости по id
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])