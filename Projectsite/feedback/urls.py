# feedback/urls.py
from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('', views.FeedbackFormView.as_view(), name='form'),
    path('success/', views.FeedbackSuccessView.as_view(), name='success'),
    path('my/', views.UserFeedbackListView.as_view(), name='user_list'),
    path('my/<int:pk>/', views.FeedbackDetailView.as_view(), name='user_detail'),
    path('my/<int:pk>/delete/', views.UserFeedbackDeleteView.as_view(), name='user_delete'),
    path('admin/list/', views.AdminFeedbackListView.as_view(), name='admin_list'),
    path('admin/<int:pk>/reply/', views.AdminFeedbackReplyView.as_view(), name='admin_reply'),
]