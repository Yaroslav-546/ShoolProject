from django.urls import path
from .views import RegisterView, CustomLoginView, CustomLogoutView, CustomLogoutViewPage, DashboardView, ProfileView, ProfileUpdateView

# Пути
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('logout_page/', CustomLogoutViewPage.as_view(), name='logout_page'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
]