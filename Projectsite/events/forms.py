# events/forms.py
from django import forms
from .models import Event, EventRegistration
from django.core.exceptions import ValidationError
from django.utils import timezone

class EventForm(forms.ModelForm):
    """
    Форма для создания/редактирования события (только для админов)
    """
    class Meta:
        model = Event
        fields = ['title', 'event_type', 'description', 'start_date', 'end_date',
                  'registration_deadline', 'location', 'address', 'max_participants',
                  'is_active', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'event_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'registration_deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        registration_deadline = cleaned_data.get('registration_deadline')

        if start_date and end_date and start_date >= end_date:
            raise ValidationError('Дата окончания должна быть позже даты начала')

        if registration_deadline and start_date and registration_deadline >= start_date:
            raise ValidationError('Срок регистрации должен быть раньше начала события')

        return cleaned_data


class EventRegistrationForm(forms.ModelForm):
    """
    Форма записи на событие
    """
    class Meta:
        model = EventRegistration
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if not self.user:
            raise ValidationError('Пользователь не авторизован')

        if not self.event:
            raise ValidationError('Событие не указано')

        existing_registration = EventRegistration.objects.filter(
            event=self.event,
            user=self.user
        ).first()

        if existing_registration:
            if existing_registration.status == 'cancelled':
                existing_registration.delete()
            else:
                raise ValidationError(
                    f'Вы уже записаны на это событие. '
                    f'Статус: {existing_registration.get_status_display()}. '
                    f'Дата записи: {existing_registration.registration_date.strftime("%d.%m.%Y %H:%M")}'
                )

        if not self.event.is_registration_open():
            raise ValidationError('Регистрация на это событие закрыта')

        return cleaned_data

    def save(self, commit=True):
        registration = super().save(commit=False)
        registration.user = self.user
        registration.event = self.event
        registration.full_name = self.user.get_full_name()
        registration.grade = self.user.grade or ''
        registration.email = self.user.email

        if commit:
            registration.save()

        return registration
