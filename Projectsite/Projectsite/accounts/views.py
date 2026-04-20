from django.views.generic import CreateView, DetailView, UpdateView, TemplateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .forms import CustomUserCreationForm, ProfileUpdateForm, EmailOrUsernameAuthenticationForm
from .models import CustomUser
from django.contrib.auth import login
from .forms import PasswordResetRequestForm, CustomSetPasswordForm
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from django.db.models import Q


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """Отправка письма для верификации после успешной регистрации"""
        response = form.save(commit=True, request=self.request) # type: ignore
        messages.success(
            self.request,
            'Регистрация прошла успешно! '
            'На вашу электронную почту отправлено письмо с ссылкой для подтверждения.'
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Обработка ошибок формы"""
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)

class VerifyEmailView(TemplateView):
    template_name = 'registration/verify_email.html'
    
    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        
        try:
            user = CustomUser.objects.get(email_verification_token=token)
            if not user.email_verified:
                user.email_verified = True
                user.is_active = True  # Активируем аккаунт
                user.email_verification_token = None  # Удаляем использованный токен
                user.save()
                
                messages.success(
                    request,
                    'Ваш email успешно подтверждён! Теперь вы можете войти в свой аккаунт.'
                )
            else:
                messages.info(request, 'Ваш email уже был подтверждён ранее.')
                
        except CustomUser.DoesNotExist:
            messages.error(request, 'Неверная или устаревшая ссылка для подтверждения.')
        
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подтверждение email'
        return context

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = EmailOrUsernameAuthenticationForm  # Используем нашу форму
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        if username and password:
            # Проверяем существует ли пользователь
            try:
                from .models import CustomUser
                user = CustomUser.objects.get(
                    Q(username__iexact=username) | Q(email__iexact=username)
                )
                
                if not user.check_password(password):
                    messages.error(self.request, _("Неверный пароль. Попробуйте еще раз."))
                elif not user.is_active:
                    messages.error(self.request, _("Ваш аккаунт не активирован. Проверьте почту с письмом активации"))
                elif not user.email_verified:
                    messages.warning(self.request, _("Email не подтвержден. Проверьте вашу почту."))
                    
            except CustomUser.DoesNotExist:
                messages.error(self.request, _("Пользователь с такими данными не найден."))
        
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем информацию о том, что можно вводить email
        context['login_hint'] = 'Вы можете использовать логин или email для входа'
        return context

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

class PasswordResetView(FormView):
    """Представление для запроса сброса пароля"""
    template_name = 'registration/password_reset.html'
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy('password-reset-done')
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = CustomUser.objects.get(email=email)
        
        # Отправка письма со ссылкой для сброса
        user.send_password_reset_email(self.request)
        
        messages.info(
            self.request,
            f'На адрес {email} отправлено письмо с инструкциями по сбросу пароля.'
        )
        return super().form_valid(form)

class PasswordResetDoneView(TemplateView):
    """Страница подтверждения отправки письма"""
    template_name = 'registration/password_reset_done.html'

class PasswordResetConfirmView(FormView):
    """Представление для установки нового пароля"""
    template_name = 'registration/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password-reset-complete')
    
    def dispatch(self, request, *args, **kwargs):
        # Проверяем токен
        self.token = kwargs.get('token')
        try:
            self.user = CustomUser.objects.get(reset_password_token=self.token)
            if not self.user.is_password_reset_token_valid():
                messages.error(request, 'Ссылка для сброса пароля устарела.')
                return redirect('password-reset')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Неверная ссылка для сброса пароля.')
            return redirect('password-reset')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['validlink'] = True
        context['user'] = self.user
        return context
    
    def form_valid(self, form):
        # Сохраняем новый пароль
        form.save()
        
        # Очищаем токен
        self.user.clear_password_reset_token()
        
        # Автоматически логиним пользователя
        login(self.request, self.user)
        
        messages.success(
            self.request,
            f'Пароль успешно изменён! Вы вошли в систему как {self.user.get_full_name()}.'
        )
        return super().form_valid(form)

class PasswordResetCompleteView(TemplateView):
    """Страница успешного сброса пароля"""
    template_name = 'registration/password_reset_complete.html'