from django.urls import path
from . import views

app_name = 'circles'

urlpatterns = [
    path('create/', views.CircleCreateView.as_view(), name='circle_create'),
    path('<slug:slug>/edit/', views.CircleUpdateView.as_view(), name='circle_edit'),
    path('<slug:slug>/delete/', views.CircleDeleteView.as_view(), name='circle_delete'),

    path('', views.CirclesListView.as_view(), name='circles_list'),
    path('<slug:slug>/', views.CircleDetailView.as_view(), name='circle_detail'),
]