# events/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic.edit import FormMixin

from .models import Event, EventRegistration
from .forms import EventForm, EventRegistrationForm
from .utils import send_registration_email, send_cancellation_email, send_waiting_list_email, send_confirmation_from_waiting_email

class StaffRequiredMixin(UserPassesTestMixin):
    """Миксин для проверки, является ли пользователь сотрудником (админом)"""
    def test_func(self):
        return self.request.user.is_staff


class EventListView(LoginRequiredMixin, ListView):
    """
    Список всех событий (турниров)
    """
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()

        self.event_type = self.request.GET.get('type', '')
        self.status = self.request.GET.get('status', 'upcoming')

        if self.event_type:
            queryset = queryset.filter(event_type=self.event_type)

        now = timezone.now()
        if self.status == 'upcoming':
            queryset = queryset.filter(start_date__gt=now, is_active=True)
        elif self.status == 'ongoing':
            queryset = queryset.filter(start_date__lte=now, end_date__gte=now, is_active=True)
        elif self.status == 'past':
            queryset = queryset.filter(end_date__lt=now)
        elif self.status == 'active':
            queryset = queryset.filter(is_active=True, registration_deadline__gte=now)

        queryset = queryset.order_by('start_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_registrations = EventRegistration.objects.filter(
            user=self.request.user
        ).values('event_id', 'status')

        registrations_dict = {}
        for reg in user_registrations:
            registrations_dict[reg['event_id']] = reg['status']

        events_list = context['events']
        total_participants = sum(event.current_participants for event in events_list)
        total_free_slots = sum(event.available_slots() for event in events_list)
        total_tournaments = sum(1 for event in events_list if event.event_type == 'chess')

        context['user_registrations'] = registrations_dict
        context['event_type_choices'] = Event.EVENT_TYPES
        context['current_type'] = self.event_type
        context['current_status'] = self.status
        context['total_participants'] = total_participants
        context['total_free_slots'] = total_free_slots
        context['total_tournaments'] = total_tournaments

        return context


class EventDetailView(LoginRequiredMixin, FormMixin, DetailView):
    """
    Детальная страница события
    """
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'
    form_class = EventRegistrationForm

    def get_success_url(self):
        return reverse_lazy('events:event_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_registration = EventRegistration.objects.filter(
            event=self.object,
            user=self.request.user
        ).first()

        context['user_registration'] = user_registration
        context['available_slots'] = self.object.available_slots()
        context['is_registration_open'] = self.object.is_registration_open()
        context['now'] = timezone.now()

        return context

    def get_form(self, form_class=None):
        """Переопределяем метод для передачи пользователя и события в форму"""
        if form_class is None:
            form_class = self.get_form_class()

        # Передаем user и event в форму
        return form_class(
            **self.get_form_kwargs(),
            user=self.request.user,
            event=self.object
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'cancel' in request.POST:
            return self.cancel_registration(request)
        elif 'register' in request.POST:
            return self.register(request)

        return self.get(request, *args, **kwargs)

    def register(self, request):
        """Запись на событие"""
        form = self.get_form()

        if form.is_valid():
            cancelled_registration = EventRegistration.objects.filter(
                event=self.object,
                user=request.user,
                status='cancelled'
            ).first()

            if cancelled_registration:
                cancelled_registration.reactivate()
                messages.success(request, f'Вы успешно восстановили запись на событие "{self.object.title}"!')
                return redirect(self.get_success_url())

            registration = form.save(commit=False)

            registration.save()

            if registration.event.current_participants >= registration.event.max_participants:
                registration.status = 'waiting'
                registration.save()
                messages.info(request, f'Вы добавлены в лист ожидания на событие "{self.object.title}".')
                send_waiting_list_email(request.user, self.object, registration)
            else:
                registration.confirm_registration()
                messages.success(request, f'Вы успешно записаны на событие "{self.object.title}"!')
                send_registration_email(request.user, self.object, registration)

            return redirect(self.get_success_url())

        return self.get(request)

    def cancel_registration(self, request):
        """Отмена записи"""
        registration = EventRegistration.objects.filter(
            event=self.object,
            user=request.user
        ).first()

        if registration:
            was_confirmed = registration.status == 'confirmed'

            if was_confirmed:
                self.object.current_participants -= 1
                self.object.save()

            registration.status = 'cancelled'
            registration.save()
            messages.success(request, 'Вы успешно отменили запись на событие.')

            send_cancellation_email(request.user, self.object, registration)

            self.activate_next_from_waiting_list(request)
        else:
            messages.warning(request, 'Запись не найдена.')

        return redirect(self.get_success_url())

    def activate_next_from_waiting_list(self, request):
        """Активировать следующего из листа ожидания"""
        next_registration = EventRegistration.objects.filter(
            event=self.object,
            status='waiting'
        ).order_by('registration_date').first()

        if next_registration and self.object.current_participants < self.object.max_participants:
            next_registration.confirm_registration()
            messages.info(request, f'Участник {next_registration.full_name} перемещен из листа ожидания.')
            send_confirmation_from_waiting_email(next_registration.user, self.object, next_registration)


class EventCreateView(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    """
    Создание события (только для админов)
    """
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание события'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Событие "{self.object.title}" успешно создано.')
        return response

    def get_success_url(self):
        return reverse_lazy('events:event_detail', kwargs={'pk': self.object.pk})


class EventUpdateView(StaffRequiredMixin, LoginRequiredMixin, UpdateView):
    """
    Редактирование события (только для админов)
    """
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование события'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Событие "{self.object.title}" успешно обновлено.')
        return response

    def get_success_url(self):
        return reverse_lazy('events:event_detail', kwargs={'pk': self.object.pk})


class EventParticipantsView(StaffRequiredMixin, LoginRequiredMixin, DetailView):
    """
    Просмотр участников события (для админов)
    """
    model = Event
    template_name = 'event_participants.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_participants = EventRegistration.objects.filter(event=self.object).select_related('user')

        context['stats'] = {
            'total': all_participants.count(),
            'confirmed': all_participants.filter(status='confirmed').count(),
            'pending': all_participants.filter(status='pending').count(),
            'waiting': all_participants.filter(status='waiting').count(),
            'cancelled': all_participants.filter(status='cancelled').count(),
            'checked_in': all_participants.filter(checked_in=True).count(),
        }

        filtered_participants = all_participants

        self.status_filter = self.request.GET.get('status', '')
        if self.status_filter:
            filtered_participants = filtered_participants.filter(status=self.status_filter)

        self.search_query = self.request.GET.get('search', '')
        if self.search_query:
            filtered_participants = filtered_participants.filter(
                Q(full_name__icontains=self.search_query) |
                Q(grade__icontains=self.search_query) |
                Q(email__icontains=self.search_query) |
                Q(user__username__icontains=self.search_query)  # Добавил поиск по username
            )

        paginator = Paginator(filtered_participants, 20)
        page_number = self.request.GET.get('page')
        context['participants'] = paginator.get_page(page_number)
        context['status_filter'] = self.status_filter
        context['search_query'] = self.search_query

        return context

class EventDeleteView(StaffRequiredMixin, LoginRequiredMixin, DeleteView):
    """
    Удаление события (только для админов)
    """
    model = Event
    template_name = 'event_confirm_delete.html'
    success_url = reverse_lazy('events:event_list')

    def delete(self, request, *args, **kwargs):
        event = self.get_object()
        messages.success(request, f'Событие "{event.title}" успешно удалено.')
        return super().delete(request, *args, **kwargs)


class ParticipantCheckInView(StaffRequiredMixin, LoginRequiredMixin, View):
    """
    Отметка участника на событии (для админов)
    """
    def post(self, request, registration_id):
        registration = get_object_or_404(EventRegistration, id=registration_id)

        registration.checked_in = True
        registration.check_in_time = timezone.now()
        registration.save()

        messages.success(request, f'Участник {registration.full_name} отмечен как присутствующий.')
        return redirect('events:event_participants', pk=registration.event.pk)


class ParticipantConfirmView(StaffRequiredMixin, LoginRequiredMixin, View):
    """
    Подтверждение регистрации участника (для админов)
    """
    def post(self, request, registration_id):
        registration = get_object_or_404(EventRegistration, id=registration_id)

        if registration.status == 'pending':
            registration.confirm_registration()
            messages.success(request, f'Регистрация участника {registration.full_name} подтверждена.')
        else:
            messages.warning(request, f'Невозможно подтвердить регистрацию. Текущий статус: {registration.get_status_display()}')

        return redirect('events:event_participants', pk=registration.event.pk)