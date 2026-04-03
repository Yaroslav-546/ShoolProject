from django.shortcuts import render

class AdminAccessMiddleware:
    """Middleware для ограничения доступа к админ-панели"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Проверяем, пытается ли пользователь зайти на /admin/
        if request.path.startswith('/admin/'):
            # Если пользователь не авторизован или не является суперпользователем
            if not request.user.is_authenticated or not request.user.is_superuser:
                context = {
                    'error_code': 403,
                    'error_title': 'Доступ запрещен',
                    'error_message': 'У вас нет прав для доступа к административной панели.',
                    'user': request.user
                }
                return render(request, '403.html', context, status=403)
        
        return self.get_response(request)