from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    change_form_show_cancel_button = True
    list_fullwidth = True
    list_per_page = 25

    list_display = ['family', 'name', 'active', 'Class', 'created_at', 'user_link']
    list_filter = ['active', 'Class']
    search_fields = ['family', 'name', 'active', 'Class', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'family', 'name', 'user', 'Class', 'active']

    fieldsets = (
        ('Ученик', {
            'fields': ('user', 'family', 'name', 'Class', 'active'),
            'classes': ('wide',),
        }),
        ('Дата записи', {
            'fields': ('created_at',),
            'classes': ('wide',),
        }),
    )

    def user_link(self, obj):
        if obj.user:
            return format_html(
                '<a href="/admin/accounts/customuser/{}/change/">{}</a>',
                obj.user.id,
                obj.user.username
            )
        return '—'
    user_link.short_description = 'Пользователь'