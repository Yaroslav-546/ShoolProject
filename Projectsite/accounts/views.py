from django.views.generic import CreateView, DetailView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import CustomUser
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _

class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Регистрация прошла успешно! Теперь вы можете войти.')
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        response = super().form_invalid(form)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # Проверяем, существует ли пользователь
        if username and password:
            user = authenticate(self.request, username=username, password=password)
            if user is None:
                messages.error(self.request, _("Аккаунта с такими данными не существует. Проверьте логин и пароль."))
            elif not user.is_active:
                messages.error(self.request, _("Ваш аккаунт деактивирован. Обратитесь к администратору."))

        return response

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')

class CustomLogoutViewPage(TemplateView):
    template_name = 'registration/logout.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)