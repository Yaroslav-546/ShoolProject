from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тема обращения'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Ваше сообщение...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class AdminReplyForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['status', 'admin_reply']
        widgets = {
            'admin_reply': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Введите ответ пользователю...'
            }),
            'status': forms.Select(attrs={'class': 'form-control'})
        }