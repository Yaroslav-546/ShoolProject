# feedback/views.py
from django.views.generic import FormView, ListView, UpdateView, TemplateView, DetailView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import FeedbackForm
from .forms import AdminReplyForm
from .models import Feedback
from django.utils import timezone

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class FeedbackFormView(LoginRequiredMixin, FormView):
    """Представление для формы обратной связи"""
    template_name = 'feedback/feedback_form.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('feedback:success')

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['name'] = self.request.user.get_full_name() or self.request.user.username
            initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        # Сохраняем сообщение в базу
        feedback = form.save(commit=False)
        if self.request.user.is_authenticated:
            feedback.user = self.request.user
        feedback.save()

        messages.success(
            self.request,
            'Спасибо! Ваше сообщение отправлено. Мы ответим вам в ближайшее время.'
        )
        return super().form_valid(form)

class UserFeedbackDeleteView(LoginRequiredMixin, DeleteView):
    model = Feedback
    template_name = 'feedback/feedback_confirm_delete.html'
    success_url = reverse_lazy('feedback:user_list')

    def get_queryset(self):
        # Пользователь может удалять только свои сообщения
        return Feedback.objects.filter(email=self.request.user.email)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Сообщение успешно удалено.')
        return super().delete(request, *args, **kwargs)


class FeedbackSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'feedback/feedback_success.html'

class UserFeedbackListView(LoginRequiredMixin, ListView):
    model = Feedback
    template_name = 'feedback/user_feedback_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 10

    def get_queryset(self):
        return Feedback.objects.filter(email=self.request.user.email).order_by('-created_at')

class FeedbackDetailView(LoginRequiredMixin, DetailView):
    model = Feedback
    template_name = 'feedback/feedback_detail.html'
    context_object_name = 'feedback'

    def get_queryset(self):
        return Feedback.objects.filter(email=self.request.user.email)

class AdminFeedbackListView(StaffRequiredMixin, ListView):
    model = Feedback
    template_name = 'feedback/admin_feedback_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', '')
        return context

class AdminFeedbackReplyView(StaffRequiredMixin, UpdateView):
    model = Feedback
    form_class = AdminReplyForm
    template_name = 'feedback/admin_feedback_reply.html'
    success_url = reverse_lazy('feedback:admin_list')
    context_object_name = 'feedback'
    def form_valid(self, form):
        feedback = form.save(commit=False)
        if feedback.admin_reply and not feedback.replied_at:
            feedback.replied_at = timezone.now()

        feedback.save()
        messages.success(self.request, f'Ответ отправлен пользователю {feedback.email}')
        return super().form_valid(form)