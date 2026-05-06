from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from .models import News

@admin.register(News)
class NewsAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    change_form_show_cancel_button = True
    list_fullwidth = True
    list_per_page = 25

    readonly_fields = ('date',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'image'),
            'classes': ('wide',),
        }),
        ('Содержание новости', {
            'fields': ('body',),
            'classes': ('wide',),
        }),
        ('Дата публикации', {
            'fields': ('date',),
            'classes': ('wide',),
        }),
    )

    formfield_overrides = {
        models.TextField: {'widget': WysiwygWidget},
    }