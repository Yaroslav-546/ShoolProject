from django.shortcuts import render, get_object_or_404
from .models import Circle
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

class StaffRequiredMixin(UserPassesTestMixin):
    """Миксин для проверки прав администратора"""

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для этого действия')
        return redirect('circles:circles_list')

class CirclesListView(ListView):
    model = Circle
    template_name = 'circles/circles_list.html'
    context_object_name = 'circles'
    paginate_by = 12

    def get_queryset(self):
        queryset = Circle.objects.filter(is_active=True).order_by('order', 'name')

        # Поиск
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(teacher__icontains=search_query) |
                Q(grade__icontains=search_query)
            )

        # Фильтр по дню недели
        selected_day = self.request.GET.get('day', '')
        if selected_day:
            circles = []
            for circle in queryset:
                if selected_day in circle.get_days_list():
                    circles.append(circle.id)
            queryset = queryset.filter(id__in=circles)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_day'] = self.request.GET.get('day', '')
        return context

class CircleDetailView(DetailView):
    """Детальная страница кружка"""
    model = Circle
    template_name = 'circles/circle_detail.html'
    context_object_name = 'circle'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Circle, slug=slug, is_active=True)

class CircleCreateView(StaffRequiredMixin, CreateView):
    """Создание кружка (только для админов)"""
    model = Circle
    template_name = 'circles/circle_form.html'
    fields = ['name', 'slug', 'icon', 'grade', 'room', 'teacher',
              'description', 'schedule', 'days', 'content', 'order']
    success_url = reverse_lazy('circles:circles_list')

    def form_valid(self, form):
        messages.success(self.request, f'Кружок "{form.instance.name}" успешно создан!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание кружка'
        context['button_text'] = 'Создать'
        return context


class CircleUpdateView(StaffRequiredMixin, UpdateView):
    """Редактирование кружка (только для админов)"""
    model = Circle
    template_name = 'circles/circle_form.html'
    fields = ['name', 'slug', 'icon', 'grade', 'room', 'teacher',
              'description', 'schedule', 'days', 'content', 'order']
    success_url = reverse_lazy('circles:circles_list')

    def form_valid(self, form):
        messages.success(self.request, f'Кружок "{form.instance.name}" успешно обновлён!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование кружка'
        context['button_text'] = 'Сохранить'
        return context


class CircleDeleteView(StaffRequiredMixin, DeleteView):
    """Удаление кружка (только для админов)"""
    model = Circle
    template_name = 'circles/circle_confirm_delete.html'
    success_url = reverse_lazy('circles:circles_list')

    def delete(self, request, *args, **kwargs):
        circle = self.get_object()
        messages.success(request, f'Кружок "{circle.name}" успешно удалён!')
        return super().delete(request, *args, **kwargs)