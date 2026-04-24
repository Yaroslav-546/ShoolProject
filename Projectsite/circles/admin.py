from django.contrib import admin
from django import forms
from .models import Circle

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
class CircleAdmin(admin.ModelAdmin):
    form = CircleAdminForm
    list_display = ['name', 'slug', 'grade', 'teacher', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'teacher', 'grade']
    search_fields = ['name', 'teacher', 'grade']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'icon', 'order', 'is_active')
        }),

        ('Детали кружка', {
            'fields': ('grade', 'room', 'teacher', 'description'),
            'classes': ('wide',),
            'description': 'Основная информация о кружке'
        }),

        ('Расписание', {
            'fields': ('schedule', 'days'),
            'classes': ('wide',),
            'description': 'Укажите дни и время занятий. Формат schedule: [{"day": "monday", "time": "15:50-17:30"}]'
        }),

        ('HTML контент', {
            'fields': ('content',),
            'classes': ('wide',),
        }),
    )

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }