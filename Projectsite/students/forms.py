from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['active', 'Class']  # Только кружок и класс
        labels = {
            'active': 'Выберите кружок',
            'Class': 'Ваш класс',
        }
        widgets = {
            'active': forms.Select(attrs={'class': 'form-control form-select'}),
            'Class': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например, 10А'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProfileForm, self).__init__(*args, **kwargs)

        # Обновляем классы для полей
        for field_name in self.fields:
            if field_name != 'active':  # Для select отдельный класс
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        if self.request and self.request.user.is_authenticated:
            active = cleaned_data.get('active')
            
            if active and Profile.objects.filter(user=self.request.user, active=active).exists():
                # Получаем дату существующей записи
                existing_registration = Profile.objects.filter(
                    user=self.request.user, 
                    active=active
                ).first()
                
                raise forms.ValidationError(
                    f"Вы уже записаны на кружок '{active}'. "
                    f"Запись была сделана {existing_registration.created_at.strftime('%d.%m.%Y')}. "
                )
        return cleaned_data