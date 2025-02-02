from django.urls import path
# from . import views

from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView, HomeView, ExitView, ActivitiesView

#url ссылки и каталоги в сайте для того чтобы отображались файлы
urlpatterns = [
    path('exit/', ExitView.as_view(), name='exit'),
    path('activities', ActivitiesView.as_view(), name='activities'),
    path('post/<int:pk>/delete/', BlogDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/edit/', BlogUpdateView.as_view(), name="post_edit"),
    path('post/new/', BlogCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('', HomeView.as_view() , name='index'),
    path('news/', BlogListView.as_view(), name='news'),
]