def admin_stats(request):
    """Добавляет статистику для админ-панели"""
    if request.path.startswith('/admin/'):
        try:
            from django.contrib.auth import get_user_model
            from events.models import Event
            from students.models import Profile
            from events.models import EventRegistration
            
            # Получаем кастомную модель пользователя
            User = get_user_model()
            
            user_count = User.objects.count()
            event_count = Event.objects.count()
            circle_count = Profile.objects.values('active').distinct().count()
            registration_count = EventRegistration.objects.count()
            
            return {
                'user_count': user_count,
                'event_count': event_count,
                'circle_count': circle_count,
                'registration_count': registration_count,
            }
        except Exception as e:
            print(f"Error loading stats: {e}")
            return {
                'user_count': 0,
                'event_count': 0,
                'circle_count': 0,
                'registration_count': 0,
            }
    return {}