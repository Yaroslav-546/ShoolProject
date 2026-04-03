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
            'description': '''
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
                    <strong>📝 Инструкция по созданию страницы кружка:</strong><br><br>
                    <strong>1. Базовый шаблон для копирования:</strong>
                    <textarea rows="15" style="width: 100%; font-family: monospace; font-size: 12px; margin: 10px 0;" readonly>
<div class="container py-3 py-md-4">
    <!-- Hero Section -->
    <div class="circle-hero-section circle-fade-in-up">
        <div class="row align-items-center">
            <div class="col-md-8">
                <div class="circle-hero-icon">
                    <i class="fas fa-chess-queen"></i>
                </div>
                <h1 class="circle-hero-title">Название кружка</h1>
                <p class="circle-hero-subtitle">Краткое описание</p>
            </div>
            <div class="col-md-4 text-md-end">
                <i class="fas fa-graduation-cap fa-4x opacity-25"></i>
            </div>
        </div>
    </div>

    <!-- Основная информация -->
    <div class="circle-main-card">
        <div class="circle-card-header-red">
            <h3><i class="fas fa-info-circle"></i> О кружке</h3>
        </div>
        <div class="circle-card-body">
            <div class="circle-info-grid">
                <div class="circle-info-block">
                    <div class="circle-info-block-title">
                        <i class="fas fa-bullseye"></i>
                        <h4>Цель кружка</h4>
                    </div>
                    <div class="circle-info-block-text">
                        <p>Текст цели...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Ключевые навыки -->
    <div class="circle-main-card">
        <div class="circle-card-header-red">
            <h3><i class="fas fa-cogs"></i> Ключевые навыки</h3>
        </div>
        <div class="circle-card-body">
            <div class="circle-features-grid">
                <div class="circle-feature-item">
                    <i class="fas fa-brain"></i>
                    <span>Навык 1</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Преимущества -->
    <div class="circle-main-card">
        <div class="circle-card-header-red">
            <h3><i class="fas fa-star"></i> Преимущества</h3>
        </div>
        <div class="circle-card-body">
            <div class="row g-4">
                <div class="col-md-4">
                    <div class="circle-info-block text-center">
                        <i class="fas fa-brain fa-3x mb-3" style="color: rgb(240, 59, 59);"></i>
                        <h5 class="fw-bold">Заголовок</h5>
                        <p class="small text-muted">Описание</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Галерея -->
    <div class="circle-main-card">
        <div class="circle-card-header-red">
            <h3><i class="fas fa-images"></i> Фотогалерея</h3>
        </div>
        <div class="circle-card-body">
            <div class="circle-gallery-grid">
                <div class="circle-gallery-item" data-fancybox="gallery" data-src="/static/Images/photo.jpg">
                    <img src="/static/Images/photo.jpg" alt="Фото">
                    <div class="circle-gallery-overlay">
                        <i class="fas fa-search-plus"></i> Увеличить
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Кнопка записи -->
    <div class="text-center">
        <a href="{% url 'sign_up_active' %}" class="circle-btn-main circle-btn-primary-red">
            <i class="fas fa-pen-alt me-2"></i>Записаться на кружок
        </a>
    </div>
</div>
                    </textarea>
                    <br>
                    <strong>Доступные CSS классы:</strong> circle-hero-section, circle-main-card, 
                    circle-card-header-red, circle-info-block, circle-features-grid, 
                    circle-gallery-grid, circle-feature-item, circle-btn-main<br>
                    <strong>Пример иконок Font Awesome:</strong> fas fa-chess-queen, fas fa-code, fas fa-robot, fas fa-brain, fas fa-cogs, fas fa-star, fas fa-images<br>
                    <strong>Для изображений используйте путь:</strong> /static/Images/название_файла.jpg<br>
                    <strong>Важно:</strong> Не используйте теги {% raw %}{% static %}{% endraw %} в HTML контенте - пишите полный путь /static/...
                </div>
            '''
        }),
    )
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }