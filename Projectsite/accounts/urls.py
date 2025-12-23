from django.urls import path
from .views import RegisterView, CustomLoginView, CustomLogoutView, CustomLogoutViewPage, DashboardView, ProfileView, ProfileUpdateView, VerifyEmailView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView  
# Пути
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('logout_page/', CustomLogoutViewPage.as_view(), name='logout_page'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password-reset-complete'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('password-reset/<str:token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
   
]