from django.contrib import admin
from .models import Profile
 
# Регистрация панели и стилизация названия
admin.site.register(Profile)
admin.site.site_title = 'Админ-панель'
admin.site.site_header = 'Админ-панель'