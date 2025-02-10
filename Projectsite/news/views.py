from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import News
# Подключение различных модулей

# Пример модели
class BlogListView(ListView):
    model = News
    template_name = 'news.html'

class BlogDetailView(DetailView):
    model = News
    template_name = 'post_detail.html'

class BlogCreateView(CreateView):
    model = News
    template_name = 'post_new.html'
    fields = ['title', 'author', 'body', 'image']

class BlogUpdateView(UpdateView):
    model = News
    template_name = "post_edit.html"
    fields = ["title", "body", 'image']

class BlogDeleteView(DeleteView):
    model = News
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')

class HomeView(ListView):
    model = News
    template_name = 'index.html'

class ExitView(ListView):
    model = News
    template_name = 'exit.html'

class ActivitiesView(ListView):
    model = News
    template_name = 'activities.html'

class ActiveProgrammingView(ListView):
    model = News
    template_name = 'active-programming.html'

class ActiveRoboticsView(ListView):
    model = News
    template_name = 'active-robotics.html'

class ActiveChessView(ListView):
    model = News
    template_name = 'active-chess.html'

class ActiveGeoInformaticsView(ListView):
    model = News
    template_name = 'active-geoinformatics.html'

class ActiveObjzView(ListView):
    model = News
    template_name = 'active-objz.html'

class ActivePhotoVideoView(ListView):
    model = News
    template_name = 'active-photo-video.html'

class ActiveVirtualRealityView(ListView):
    model = News
    template_name = 'active-virtualreality.html'

class ActivePromDesignView(ListView):
    model = News
    template_name = 'active-promdesign.html'

class ActiveGalleryView(ListView):
    model = News
    template_name = 'gallery.html'

class ActiveAchievementsView(ListView):
    model = News
    template_name = 'achievements.html'