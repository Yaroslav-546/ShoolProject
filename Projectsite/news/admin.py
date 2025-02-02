from django.contrib import admin
from .models import News

#Админ панель регистрация
admin.site.register(News)
# Стилизация: Название панели
admin.site.site_title = 'Админ-панель'
admin.site.site_header = 'Админ-панель'