from .forms import ProfileForm
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import ListView
from .models import Profile
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib import messages

class RedirectPermissionRequiredMixin(PermissionRequiredMixin):
    login_url = reverse_lazy('error403')

    def handle_no_permission(self):
        return redirect(self.get_login_url())
    
class LoginRequiredMixinCustom(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Для доступа к этой странице необходимо войти в систему.")
        return super().dispatch(request, *args, **kwargs)

class SuccessView(TemplateView):
    template_name = 'success.html'

class ProfileFormView(LoginRequiredMixinCustom, CreateView):
    form_class = ProfileForm
    template_name = 'registration_activities.html'
    success_url = reverse_lazy('my_registrations')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            form.add_error(None, "Для записи на кружок необходимо авторизоваться")
            return self.form_invalid(form)
        
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.family = self.request.user.last_name
        profile.name = self.request.user.first_name
        
        if Profile.objects.filter(user=self.request.user, active=profile.active).exists():
            print("No")
            existing_reg = Profile.objects.filter(
                user=self.request.user, 
                active=profile.active
            ).first()
            messages.error(
                self.request, 
                f"❌ Не удалось записаться на кружок '{profile.active}'. "
                f"Вы уже записаны на этот кружок с {existing_reg.created_at.strftime('%d.%m.%Y')}."
            )
            return self.form_invalid(form)
            
        profile.save()
        messages.success(self.request, f"✅ Вы успешно записались на кружок '{profile.active}'")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Добавляем сообщение об ошибке для невалидной формы
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    if "уже записаны" in error:
                        messages.error(self.request, error)
                    else:
                        messages.warning(self.request, f"Пожалуйста, исправьте ошибки в форме: {error}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['existing_registrations'] = Profile.objects.filter(
                user=self.request.user
            )
        return context

class MyRegistrationsView(LoginRequiredMixinCustom, ListView):
    model = Profile
    template_name = 'my_registrations.html'
    context_object_name = 'registrations'
    
    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user).order_by('-created_at')

class RegistrationDeleteView(LoginRequiredMixinCustom, DeleteView):
    model = Profile
    template_name = 'registration_confirm_delete.html'
    success_url = reverse_lazy('my_registrations')
    
    def get_queryset(self):
        # Пользователь может удалять только свои записи
        return Profile.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Запись на кружок успешно удалена")
        return super().delete(request, *args, **kwargs)

class StudentsListView(RedirectPermissionRequiredMixin, ListView):
    model = Profile
    template_name = 'students.html'
    permission_required = ('auth.view_user')
