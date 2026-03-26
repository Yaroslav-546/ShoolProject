from django.urls import path
from .views import SuccessView, ProfileFormView, StudentsListView, MyRegistrationsView, RegistrationDeleteView, ActivitiesView, ActiveProgrammingView, ActiveRoboticsView, ActiveChessView, ActiveGeoInformaticsView, ActiveObjzView, ActivePhotoVideoView, ActiveVirtualRealityView, ActivePromDesignView

# Пути
urlpatterns = [
    path('sign_up_active/', ProfileFormView.as_view(), name='sign_up_active'),
    path('success/', SuccessView.as_view(), name='success'),
    path('studentslist/', StudentsListView.as_view(), name='studentslist'),
    path('my_registrations/', MyRegistrationsView.as_view(), name='my_registrations'),
    path('registration/<int:pk>/delete/', RegistrationDeleteView.as_view(), name='registration_delete'),
    path('activities/active-robotics', ActiveRoboticsView.as_view(), name='active-robotics'),
    path('activities/active-chess', ActiveChessView.as_view(), name='active-chess'),
    path('activities/active-geoinformatics', ActiveGeoInformaticsView.as_view(), name='active-geoinformatics'),
    path('activities/active-objz', ActiveObjzView.as_view(), name='active-objz'),
    path('activities/active-photo-video', ActivePhotoVideoView.as_view(), name='active-photo-video'),
    path('activities/active-virtualreality', ActiveVirtualRealityView.as_view(), name='active-virtualreality'),
    path('activities/active-programming', ActiveProgrammingView.as_view(), name='active-programming'),
    path('activities/active-promdesign', ActivePromDesignView.as_view(), name='active-promdesign'),
    path('activities', ActivitiesView.as_view(), name='activities'),
]