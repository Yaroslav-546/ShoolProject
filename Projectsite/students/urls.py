from django.urls import path
from .views import SuccessView, ProfileFormView, StudentsListView, MyRegistrationsView, RegistrationDeleteView

# Пути
urlpatterns = [
    path('sign_up_active/', ProfileFormView.as_view(), name='sign_up_active'),
    path('success/', SuccessView.as_view(), name='success'),
    path('studentslist/', StudentsListView.as_view(), name='studentslist'),
    path('my_registrations/', MyRegistrationsView.as_view(), name='my_registrations'),
    path('registration/<int:pk>/delete/', RegistrationDeleteView.as_view(), name='registration_delete'),
]