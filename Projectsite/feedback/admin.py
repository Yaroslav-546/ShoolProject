from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject', 'status', 'created_at', 'reply_status']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'replied_at']
    fieldsets = (
        ('Пользователь', {'fields': ('user', 'name', 'email')}),
        ('Сообщение', {'fields': ('subject', 'message')}),
        ('Ответ', {'fields': ('admin_reply', 'status', 'replied_at')}),
        ('Даты', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )

    def reply_status(self, obj):
        if obj.admin_reply:
            return "✓ Ответ отправлен"
        return "⏳ Ожидает ответа"
    reply_status.short_description = 'Статус ответа'