from django.shortcuts import render
from .forms import ProfileForm
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.views.generic import ListView

from .models import Profile

# View для того чтобы файлы отображались, т.е здесь указываешь файл и от чего наследуешь для работы

# Ненужно сначала создавал для формы записи потом заменил на класс
def profile_view(request):
    form = ProfileForm()
    return render(request, 'profile.html', {'form': form})

class SuccessView(TemplateView):
    template_name = 'success.html'

class ProfileFormView(CreateView):
    form_class = ProfileForm
    template_name = 'profile.html'
    success_url = reverse_lazy('success')

class StudentsListView(ListView):
    model = Profile
    template_name = 'students.html'
