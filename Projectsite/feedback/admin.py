from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget 
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    change_form_show_cancel_button = True
    list_fullwidth = True
    list_per_page = 25

    list_display = ['id', 'name', 'email', 'subject', 'status', 'created_at', 'reply_status']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'replied_at', 'user', 'name', 'email', 'subject', 'message']

    fieldsets = (
        ('Пользователь', {
            'fields': ('user', 'name', 'email'),
            'classes': ('wide',),
        }),
        ('Сообщение', {
            'fields': ('subject', 'message'),
            'classes': ('wide',),
        }),
        ('Ответ администратора', {
            'fields': ('admin_reply', 'status', 'replied_at'),
            'classes': ('wide',),
        }),
        ('Даты', {
            'fields': ('created_at',),
            'classes': ('collapse', 'wide'),
        }),
    )

    def reply_status(self, obj):
        if obj.admin_reply:
            return "✅ Ответ отправлен"
        return "⏳ Ожидает ответа"
    reply_status.short_description = 'Статус ответа'
    reply_status.admin_order_field = 'replied_at'