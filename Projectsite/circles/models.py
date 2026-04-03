from django.db import models

class Circle(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Понедельник'),
        ('tuesday', 'Вторник'),
        ('wednesday', 'Среда'),
        ('thursday', 'Четверг'),
        ('friday', 'Пятница'),
        ('saturday', 'Суббота'),
        ('sunday', 'Воскресенье'),
    ]

    name = models.CharField('Название кружка', max_length=200)
    slug = models.SlugField('URL', max_length=100, unique=True, blank=True)
    icon = models.CharField('Иконка Font Awesome', max_length=50, default='fas fa-chalkboard')
    grade = models.CharField('Классы', max_length=100, help_text='Например: 5-11 классы')
    room = models.CharField('Кабинет', max_length=10)
    teacher = models.CharField('Преподаватель', max_length=100)
    description = models.TextField('Описание', blank=True, null=True)

    # Расписание в формате JSON
    schedule = models.JSONField('Расписание', default=list,
                                 help_text='Формат: [{"day": "monday", "time": "15:50-17:30"}, ...]')

    # Исправлено: help_content -> help_text
    content = models.TextField('HTML контент страницы', blank=True,
                                help_text='Вставляйте HTML код')

    # Дни недели для фильтрации
    days = models.CharField('Дни недели', max_length=200, blank=True, null=True,
                            help_text='Дни через запятую: monday,friday')

    # Порядок сортировки
    order = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Кружок'
        verbose_name_plural = 'Кружки'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_days_list(self):
        """Получить список дней недели"""
        if self.days:
            return self.days.split(',')
        return []

    def get_schedule_display(self):
        """Получить расписание для отображения"""
        schedule_list = []
        for item in self.schedule:
            day_name = dict(self.DAYS_OF_WEEK).get(item.get('day'), item.get('day'))
            schedule_list.append(f"{day_name} {item.get('time', '')}")
        return schedule_list