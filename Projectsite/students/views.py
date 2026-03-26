from .forms import ProfileForm
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import ListView
from .models import Profile
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Count

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
    context_object_name = 'object_list'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        # Поиск по фамилии, имени или классу
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(family__icontains=search_query) |
                Q(name__icontains=search_query) |
                Q(Class__icontains=search_query)
            )

        # Фильтр по кружку
        circle_filter = self.request.GET.get('circle', '')
        if circle_filter:
            queryset = queryset.filter(active=circle_filter)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем все уникальные кружки для фильтра
        circles = Profile.objects.values_list('active', flat=True).distinct()

        # Статистика
        total_students = self.get_queryset().count()
        total_circles = Profile.objects.values('active').distinct().count()

        # Среднее количество учеников на кружок
        if total_circles > 0:
            avg_per_circle = round(total_students / total_circles, 1)
        else:
            avg_per_circle = 0

        context['search_query'] = self.request.GET.get('search', '')
        context['selected_circle'] = self.request.GET.get('circle', '')
        context['circles'] = circles
        context['total_students'] = total_students
        context['total_circles'] = total_circles
        context['avg_per_circle'] = avg_per_circle

        return context

class ActivitiesView(TemplateView):
    template_name = 'activities.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Данные о кружках
        all_circles = [
            {
                'name': 'Робототехника, старшая группа',
                'url': 'activities/active-robotics',
                'icon': 'fas fa-robot',
                'grade': '5-11 классы',
                'schedule': ['Пн 15:50-17:30', 'Пт 15:50-17:30'],
                'days': ['monday', 'friday'],
                'room': '9',
                'teacher': 'Малышева И.А.'
            },
            {
                'name': 'Геоинформатика',
                'url': 'activities/active-geoinformatics',
                'icon': 'fas fa-map',
                'grade': '7-8 классы',
                'schedule': ['Пн 15:40-17:10', 'Ср 15:40-17:10'],
                'days': ['monday', 'wednesday'],
                'room': '9',
                'teacher': 'Малышева И.А.'
            },
            {
                'name': 'Робототехника, младшая группа',
                'url': 'activities/active-robotics',
                'icon': 'fas fa-microchip',
                'grade': '1-4 классы',
                'schedule': ['Пн 14:00-15:40', 'Пт 14:00-15:40'],
                'days': ['monday', 'friday'],
                'room': '9',
                'teacher': 'Малышева И.А.'
            },
            {
                'name': 'Промышленный дизайн',
                'url': 'activities/active-promdesign',
                'icon': 'fas fa-drafting-compass',
                'grade': '5б, 5в, 5а',
                'schedule': ['Вт 12:15-12:50', 'Чт 13:00-13:35'],
                'days': ['tuesday', 'thursday'],
                'room': '9',
                'teacher': 'Малышева И.А.'
            },
            {
                'name': 'Виртуальная и дополненная реальность',
                'url': 'activities/active-virtualreality',
                'icon': 'fas fa-vr-cardboard',
                'grade': '6 класс',
                'schedule': ['Сб 12:30-13:50'],
                'days': ['saturday'],
                'room': '9',
                'teacher': 'Малышева И.А.'
            },
            {
                'name': 'Программирование',
                'url': 'activities/active-programming',
                'icon': 'fas fa-code',
                'grade': '8 класс',
                'schedule': ['Ср 15:00-16:30'],
                'days': ['wednesday'],
                'room': '18',
                'teacher': 'Бекетова Т.И.'
            },
            {
                'name': 'Фото и видеосъёмка',
                'url': 'activities/active-photo-video',
                'icon': 'fas fa-camera',
                'grade': '5-9 классы',
                'schedule': ['Вт 14:30-16:00', 'Пт 14:30-16:00'],
                'days': ['tuesday', 'friday'],
                'room': '18',
                'teacher': 'Бекетова Т.И.'
            },
            {
                'name': 'Шахматы',
                'url': 'activities/active-chess',
                'icon': 'fas fa-chess-queen',
                'grade': '3-7 классы',
                'schedule': ['Чт 13:00-14:20'],
                'days': ['thursday'],
                'room': '9',
                'teacher': 'Седов К.И.'
            },
            {
                'name': 'ОБЖ',
                'url': 'activities/active-objz',
                'icon': 'fas fa-shield-alt',
                'grade': '4 класс',
                'schedule': ['Пн 13:45-14:20'],
                'days': ['monday'],
                'room': '10',
                'teacher': 'Дунаев А.П.'
            },
        ]

        # Получаем параметры фильтрации
        search_query = self.request.GET.get('search', '')
        selected_day = self.request.GET.get('day', '')

        # Фильтрация
        circles = all_circles

        # Поиск по названию, преподавателю или классу
        if search_query:
            circles = [c for c in circles if
                      search_query.lower() in c['name'].lower() or
                      search_query.lower() in c['teacher'].lower() or
                      search_query.lower() in c['grade'].lower()]

        # Фильтр по дню недели
        if selected_day:
            circles = [c for c in circles if selected_day in c['days']]

        context['circles'] = circles
        context['search_query'] = search_query
        context['selected_day'] = selected_day

        return context

class ActiveProgrammingView(TemplateView):
    template_name = 'active-programming.html'

class ActiveRoboticsView(TemplateView):
    template_name = 'active-robotics.html'

class ActiveChessView(TemplateView):
    template_name = 'active-chess.html'

class ActiveGeoInformaticsView(TemplateView):
    template_name = 'active-geoinformatics.html'

class ActiveObjzView(TemplateView):
    template_name = 'active-objz.html'

class ActivePhotoVideoView(TemplateView):
    template_name = 'active-photo-video.html'

class ActiveVirtualRealityView(TemplateView):
    template_name = 'active-virtualreality.html'

class ActivePromDesignView(TemplateView):
    template_name = 'active-promdesign.html'
