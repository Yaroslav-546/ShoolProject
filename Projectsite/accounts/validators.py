from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_password_length(value):
    if len(value) < 8:
        raise ValidationError(
            _("Пароль слишком короткий. Он должен содержать не менее 8 символов."),
            code='password_too_short',
        )