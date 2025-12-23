from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Бэкенд аутентификации, позволяющий войти по email или username
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        
        if not username or not password:
            return None
        
        try:
            # Ищем пользователя по email ИЛИ username (без учета регистра)
            user = UserModel.objects.get(
                Q(email__iexact=username) | Q(username__iexact=username)
            )
        except UserModel.DoesNotExist:
            # Для безопасности создаем "пустышку", чтобы время отклика было одинаковым
            UserModel().set_password(password)
            return None
        except UserModel.MultipleObjectsReturned:
            # Если есть несколько пользователей (маловероятно), берем первого
            user = UserModel.objects.filter(
                Q(email__iexact=username) | Q(username__iexact=username)
            ).first()
        
        # Проверяем пароль и активность пользователя
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
    
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None