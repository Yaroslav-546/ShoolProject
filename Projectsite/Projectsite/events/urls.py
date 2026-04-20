from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_edit'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),  # Новый маршрут
    path('<int:pk>/participants/', views.EventParticipantsView.as_view(), name='event_participants'),
    path('participant/<int:registration_id>/check-in/', 
         views.ParticipantCheckInView.as_view(), 
         name='participant_check_in'),
    path('participant/<int:registration_id>/confirm/', 
         views.ParticipantConfirmView.as_view(), 
         name='participant_confirm'),
]