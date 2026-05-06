from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from .models import Event, EventRegistration
from django import forms

@admin.register(Event)
class EventAdmin(ModelAdmin):
    compressed_fields = True          
    warn_unsaved_form = True        
    change_form_show_cancel_button = True  
    list_fullwidth = True             
    list_per_page = 25              

    list_display = ['title', 'event_type', 'start_date', 'end_date', 'current_participants', 'max_participants']
    list_filter = ['event_type', 'is_active', 'start_date']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'start_date'
    readonly_fields = ['current_participants', 'created_at', 'updated_at']

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'event_type', 'description', 'image'),
            'classes': ('wide',),
        }),
        ('Даты и время', {
            'fields': ('start_date', 'end_date', 'registration_deadline'),
            'classes': ('wide',),
        }),
        ('Место проведения', {
            'fields': ('location', 'address'),
            'classes': ('wide',),
        }),
        ('Участники', {
            'fields': ('max_participants', 'current_participants'),
            'classes': ('wide',),
        }),
        ('Статус', {
            'fields': ('is_active',),
            'classes': ('wide',),
        }),
        ('Системные поля', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse', 'wide'),
        }),
    )

    formfield_overrides = {
        models.TextField: {'widget': WysiwygWidget},
        models.BooleanField: {'widget': forms.CheckboxInput(attrs={'class': 'form-checkbox'})},
    }
    

@admin.register(EventRegistration)
class EventRegistrationAdmin(ModelAdmin):
    compressed_fields = True
    list_display = ['user', 'event', 'status', 'registration_date', 'checked_in']
    list_filter = ['status', 'checked_in', 'event', 'registration_date']
    search_fields = ['user__username', 'user__email', 'full_name', 'grade']
    readonly_fields = ['registration_date', 'full_name', 'grade', 'email', 'user', 'event']
    actions = ['confirm_registrations', 'cancel_registrations', 'mark_checked_in']

    formfield_overrides = {
        models.BooleanField: {'widget': forms.CheckboxInput(attrs={'class': 'form-checkbox'})},
    }

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