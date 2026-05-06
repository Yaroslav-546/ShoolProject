from django.contrib import admin
from django import forms
from unfold.admin import ModelAdmin
from .models import Circle
from django.db import models

class CircleAdminForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 30,
            'style': 'font-family: monospace; font-size: 14px; width: 100%;',
            'placeholder': 'Вставьте HTML код страницы кружка...'
        }),
        required=False,
        help_text='Вставьте полный HTML код страницы. Используйте классы из файла active-detail.css'
    )

    class Meta:
        model = Circle
        fields = '__all__'

@admin.register(Circle)
class CircleAdmin(ModelAdmin):
    form = CircleAdminForm

    compressed_fields = True
    warn_unsaved_form = True
    change_form_show_cancel_button = True
    list_fullwidth = True
    list_per_page = 25

    list_display = ['name', 'slug', 'grade', 'teacher', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'teacher', 'grade']
    search_fields = ['name', 'teacher', 'grade']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'icon', 'order', 'is_active'),
            'classes': ('wide',),
        }),
        ('Детали кружка', {
            'fields': ('grade', 'room', 'teacher', 'description'),
            'classes': ('wide',),
            'description': 'Основная информация о кружке',
        }),
        ('Расписание', {
            'fields': ('schedule', 'days'),
            'classes': ('wide',),
            'description': 'Укажите дни и время занятий. Формат schedule: [{"day": "monday", "time": "15:50-17:30"}]',
        }),
        ('HTML контент', {
            'fields': ('content',),
            'classes': ('wide',),
        }),
    )

    formfield_overrides = {
        models.BooleanField: {'widget': forms.CheckboxInput(attrs={'class': 'form-checkbox'})},
    }

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',),
        }