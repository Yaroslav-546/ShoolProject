from django.db import models
from django.utils.text import slugify as django_slugify

def custom_slugify(value):
    value_str = str(value)

    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
        'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    }

    transliterated_chars = [translit_dict.get(ch, ch) for ch in value_str]
    
    result = ''.join(transliterated_chars)
    return django_slugify(result)

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
                            help_text='Дни недели через запятую: (например) monday,friday<br>monday-Понедельник<br>tuesday-Вторник<br>wednesday-Среда<br>thursday-Четверг<br>friday-Пятница<br>saturday-Суббота<br>sunday-Воскресенье')

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
            self.slug = custom_slugify(self.name)
            original_slug = self.slug
            counter = 1
            while Circle.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
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