from .forms import ProfileForm
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import Profile
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin

class RedirectPermissionRequiredMixin(PermissionRequiredMixin):
    login_url = reverse_lazy('error403')

    def handle_no_permission(self):
        return redirect(self.get_login_url())

class SuccessView(TemplateView):
    template_name = 'success.html'

class ProfileFormView(CreateView):
    form_class = ProfileForm
    template_name = 'profile.html'
    success_url = reverse_lazy('success')

class StudentsListView(RedirectPermissionRequiredMixin, ListView):
    model = Profile
    template_name = 'students.html'
    permission_required = ('auth.view_user')
