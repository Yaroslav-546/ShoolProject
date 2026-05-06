from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import GalleryImage
from django.db import models
from django import forms

@admin.register(GalleryImage)
class GalleryImageAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    change_form_show_cancel_button = True
    list_fullwidth = True
    list_per_page = 25

    list_display = ['title', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'image'),
            'classes': ('wide',),
        }),
        ('Настройки отображения', {
            'fields': ('order', 'is_active'),
            'classes': ('wide',),
        }),
        ('Системные данные', {
            'fields': ('created_at',),
            'classes': ('collapse', 'wide'),
        }),
    )

    readonly_fields = ('created_at',)

    formfield_overrides = {
        models.BooleanField: {'widget': forms.CheckboxInput(attrs={'class': 'form-checkbox'})},
    }