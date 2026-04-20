# students/forms.py
from django import forms
from .models import Profile
from circles.models import Circle

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['active', 'Class']
        labels = {
            'active': 'Выберите кружок',
            'Class': 'Ваш класс',
        }
        widgets = {
            'active': forms.Select(attrs={'class': 'form-control form-select'}),
            'Class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например, 10А',
                'autocomplete': 'class-name'
            })
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Базовый queryset активных кружков, отсортированный по порядку
        circles_qs = Circle.objects.filter(is_active=True).order_by('order', 'name')

        # Если пользователь авторизован, исключаем кружки, на которые он уже записан
        if self.request and self.request.user.is_authenticated:
            registered_circles_names = Profile.objects.filter(
                user=self.request.user
            ).values_list('active', flat=True)
            circles_qs = circles_qs.exclude(name__in=registered_circles_names)

        # Формируем choices: пустой пункт + названия доступных кружков
        choices = [('', '---------')] + [(circle.name, circle.name) for circle in circles_qs]
        self.fields['active'].choices = choices

        # Если пользователь уже авторизован и у него есть класс, подставляем его
        if self.request and self.request.user.is_authenticated:
            user = self.request.user
            if user.grade:
                self.fields['Class'].initial = user.grade
                self.fields['Class'].widget.attrs['readonly'] = True

        # Обновляем классы для всех полей (кроме select, он уже имеет свой класс)
        for field_name in self.fields:
            if field_name != 'active':
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        if self.request and self.request.user.is_authenticated:
            active_name = cleaned_data.get('active')
            if active_name and Profile.objects.filter(user=self.request.user, active=active_name).exists():
                existing_registration = Profile.objects.filter(
                    user=self.request.user,
                    active=active_name
                ).first()
                raise forms.ValidationError(
                    f"Вы уже записаны на кружок '{active_name}'. "
                    f"Запись была сделана {existing_registration.created_at.strftime('%d.%m.%Y')}."
                )
        return cleaned_data