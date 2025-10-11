from django.contrib import admin
from .models import CustomUser
 
admin.site.register(CustomUser)
admin.site.site_title = 'Админ-панель'
admin.site.site_header = 'Админ-панель'