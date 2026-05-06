from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from .models import CustomUser
from django.db import models
from django import forms

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    change_form_show_cancel_button = True
    list_fullwidth = True
    list_per_page = 25

    list_display = ('username', 'email', 'first_name', 'last_name', 'patronymic', 'grade', 'is_staff', 'email_verified')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'email_verified')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'patronymic')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {
            'fields': ('first_name', 'last_name', 'patronymic', 'email', 'grade', 'avatar')
        }),
        ('Статусы', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'email_verified')
        }),
        ('Токены и даты', {
            'fields': ('email_verification_token', 'reset_password_token', 'reset_password_expires', 'last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('last_login', 'date_joined', 'email_verification_token', 'reset_password_token', 'reset_password_expires', 'username', 'first_name', 'last_name', 'patronymic', 'grade', 'avatar')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'patronymic', 'grade'),
        }),
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return f'<img src="{obj.avatar.url}" width="40" height="40" style="border-radius: 50%;" />'
        return '—'
    avatar_preview.short_description = 'Аватар'
    avatar_preview.allow_tags = True

    formfield_overrides = {
        models.BooleanField: {'widget': forms.CheckboxInput(attrs={'class': 'form-checkbox'})},
    }
