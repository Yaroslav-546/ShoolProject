from django.urls import path
from .views import SuccessView, ProfileFormView, StudentsListView

# Пути
urlpatterns = [
    path('profile/', ProfileFormView.as_view(), name='profile'),
    path('success/', SuccessView.as_view(), name='success'),
    path('studentslist/', StudentsListView.as_view(), name='studentslist'),
]