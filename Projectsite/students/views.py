from .forms import ProfileForm
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import Profile

class SuccessView(TemplateView):
    template_name = 'success.html'

class ProfileFormView(CreateView):
    form_class = ProfileForm
    template_name = 'profile.html'
    success_url = reverse_lazy('success')

class StudentsListView(ListView):
    model = Profile
    template_name = 'students.html'
