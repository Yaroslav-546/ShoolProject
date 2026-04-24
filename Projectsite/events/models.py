from django.db import models
from django.conf import settings

class Event(models.Model):
    EVENT_TYPES = [
        ('chess', 'Шахматный турнир'),
        ('robotics', 'Соревнование по робототехнике'),
        ('programming', 'Олимпиада по программированию'),
        ('photo', 'Фотоконкурс'),
        ('other', 'Другое'),
    ]

    title = models.CharField('Название', max_length=200)
    event_type = models.CharField('Тип события', max_length=50, choices=EVENT_TYPES)
    description = models.TextField('Описание', blank=True)

    start_date = models.DateTimeField('Дата и время начала')
    end_date = models.DateTimeField('Дата и время окончания')
    registration_deadline = models.DateTimeField('Срок регистрации')

    location = models.CharField('Место проведения', max_length=200)
    address = models.CharField('Адрес', max_length=200, blank=True)

    max_participants = models.PositiveIntegerField('Максимум участников', default=50)
    current_participants = models.PositiveIntegerField('Текущее количество участников', default=0)
    is_active = models.BooleanField('Активно', default=True)
    image = models.ImageField('Изображение', upload_to='events/', blank=True, null=True)

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} ({self.start_date.strftime('%d.%m.%Y')})"

    def is_registration_open(self):
        """Проверка, открыта ли регистрация"""
        from django.utils import timezone
        now = timezone.now()
        return (self.is_active and
                now <= self.registration_deadline and
                self.current_participants < self.max_participants)

    def is_past(self):
        """Проверка, прошло ли событие"""
        from django.utils import timezone
        return self.end_date < timezone.now()

    def available_slots(self):
        """Доступные места"""
        return self.max_participants - self.current_participants

    def get_map_url(self):
        if self.address and ('yandex.ru/maps' in self.address or 'maps.yandex.ru' in self.address or 'yandex.ru/map-widget' in self.address):
            return self.address
        elif self.address:
            return f"https://yandex.ru/maps/?text={self.address}"
        return None

    def is_map_link(self):
        return self.address and ('yandex.ru/maps' in self.address or 'maps.yandex.ru' in self.address or 'yandex.ru/map-widget' in self.address)

class EventRegistration(models.Model):
    """
    Модель записи на событие
    """
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
        ('waiting', 'В листе ожидания'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Событие', related_name='registrations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Участник', related_name='event_registrations')

    full_name = models.CharField('ФИО', max_length=300)
    grade = models.CharField('Класс', max_length=3)
    email = models.EmailField('Email')

    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    registration_date = models.DateTimeField('Дата регистрации', auto_now_add=True)

    checked_in = models.BooleanField('Отметка о присутствии', default=False)
    check_in_time = models.DateTimeField('Время отметки', null=True, blank=True)

    notes = models.TextField('Примечания', blank=True)

    class Meta:
        verbose_name = 'Запись на событие'
        verbose_name_plural = 'Записи на события'
        ordering = ['-registration_date']
        unique_together = ['event', 'user']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.event.title}"

    def confirm_registration(self):
        """Подтверждение регистрации"""
        self.status = 'confirmed'
        self.save()

        self.event.current_participants += 1
        self.event.save()

    def cancel_registration(self):
        """Отмена регистрации"""
        if self.status == 'confirmed':
            self.event.current_participants -= 1
            self.event.save()
        self.status = 'cancelled'
        self.save()