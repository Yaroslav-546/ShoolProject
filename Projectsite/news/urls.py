from django.urls import path
# from . import views

from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView, HomeView, ExitView, ActivitiesView, ActiveProgrammingView, ActiveRoboticsView, ActiveChessView, ActiveGeoInformaticsView, ActiveObjzView, ActivePhotoVideoView, ActiveVirtualRealityView, ActivePromDesignView

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
    path('activities/active-python', ActiveProgrammingView.as_view(), name='active-programming'),
    path('activities/active-robotics', ActiveRoboticsView.as_view(), name='active-robotics'),
    path('activities/active-chess', ActiveChessView.as_view(), name='active-chess'),
    path('activities/active-geoinformatics', ActiveGeoInformaticsView.as_view(), name='active-geoinformatics'),
    path('activities/active-objz', ActiveObjzView.as_view(), name='active-objz'),
    path('activities/active-photo-video', ActivePhotoVideoView.as_view(), name='active-photo-video'),
    path('activities/active-virtualreality', ActiveVirtualRealityView.as_view(), name='active-virtualreality'),
    path('activities/active-promdesign', ActivePromDesignView.as_view(), name='active-promdesign'),
]