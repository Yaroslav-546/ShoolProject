from django.contrib import admin
from .models import Event, EventRegistration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'start_date', 'end_date', 'current_participants', 'max_participants']
    list_filter = ['event_type', 'is_active', 'start_date']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'start_date'
    readonly_fields = ['current_participants', 'created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'event_type', 'description', 'image')
        }),
        ('Даты и время', {
            'fields': ('start_date', 'end_date', 'registration_deadline')
        }),
        ('Место проведения', {
            'fields': ('location', 'address')
        }),
        ('Участники', {
            'fields': ('max_participants', 'current_participants')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
        ('Системные поля', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status', 'registration_date', 'checked_in']
    list_filter = ['status', 'checked_in', 'event', 'registration_date']
    search_fields = ['user__username', 'user__email', 'full_name', 'grade']
    readonly_fields = ['registration_date', 'full_name', 'grade', 'email']
    actions = ['confirm_registrations', 'cancel_registrations', 'mark_checked_in']
    
    def confirm_registrations(self, request, queryset):
        for registration in queryset:
            registration.confirm_registration()
        self.message_user(request, f'{queryset.count()} записей подтверждено')
    confirm_registrations.short_description = 'Подтвердить выбранные записи'
    
    def cancel_registrations(self, request, queryset):
        for registration in queryset:
            registration.cancel_registration()
        self.message_user(request, f'{queryset.count()} записей отменено')
    cancel_registrations.short_description = 'Отменить выбранные записи'
    
    def mark_checked_in(self, request, queryset):
        from django.utils import timezone
        queryset.update(checked_in=True, check_in_time=timezone.now())
        self.message_user(request, f'{queryset.count()} участников отмечено')
    mark_checked_in.short_description = 'Отметить присутствие'