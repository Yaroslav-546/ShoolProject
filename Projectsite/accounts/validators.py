from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_password_length(value):
    if len(value) < 8:
        raise ValidationError(
            _("Пароль слишком короткий. Он должен содержать не менее 8 символов."),
            code='password_too_short',
        )

def validate_grade_contains(value):
    alphabit = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "А", "Б", "В", "Г", "а", "б", "в", "г"]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    letters = ["А", "Б", "В", "Г", "а", "б", "в", "г"]
    if len(value) == 2:
        if value[0] not in numbers or value[1] not in letters or value[0] == "0":
            raise ValidationError(
            _("Класс должен состоят из числа и буквы, например 1А"),
            code='grade_error',
            )
        
    if len(value) == 3:
        if value[0] not in numbers or value[1] not in numbers or value[2] not in letters or int(value[0] + value[1]) > 11:
            raise ValidationError(
            _("Класс должен состоят из числа и буквы, например 1А"),
            code='grade_error',
            )
    for i in value:
        if i not in alphabit or len(value) < 2:
             raise ValidationError(
            _("Класс должен состоят из числа и буквы, например 1А"),
            code='grade_error',
        )