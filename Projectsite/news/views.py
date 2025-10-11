from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import News
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django import forms
# Подключение различных модулей

# Пример модели
class BlogListView(ListView):
    model = News
    template_name = 'news.html'

class BlogDetailView(DetailView):
    model = News
    template_name = 'post_detail.html'

class RedirectPermissionRequiredMixin(PermissionRequiredMixin):
    login_url = reverse_lazy('error403')

    def handle_no_permission(self):
        return redirect(self.get_login_url())

class BlogCreateView(RedirectPermissionRequiredMixin, CreateView):
    model = News
    template_name = 'post_new.html'
    fields = ['title', 'body', 'image']
    permission_required = ('auth.add_user')

class BlogUpdateView(RedirectPermissionRequiredMixin, UpdateView):
    model = News
    template_name = "post_edit.html"
    fields = ["title", "body", 'image']
    permission_required = ('auth.change_user')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Меняем виджет для поля image
        form.fields['image'].widget = forms.FileInput(attrs={'class': 'file-input', 'accept': 'image/*'})
        # Добавляем классы к другим полям
        form.fields['title'].widget.attrs.update({'class': 'form-input'})
        form.fields['body'].widget.attrs.update({'class': 'form-textarea'})
        return form

class BlogDeleteView(RedirectPermissionRequiredMixin, DeleteView):
    model = News
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')
    permission_required = ('auth.delete_user')

class HomeView(TemplateView):
    template_name = 'index.html'

class ExitView(TemplateView):
    template_name = 'exit.html'

class Error403(TemplateView):
    template_name = '403.html'

class ActivitiesView(TemplateView):
    template_name = 'activities.html'

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

class ActiveGalleryView(TemplateView):
    template_name = 'gallery.html'

class ActiveAchievementsView(TemplateView):
    template_name = 'achievements.html'