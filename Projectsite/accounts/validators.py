from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

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

def validate_russian_name(value):
    """Проверка русских букв, дефиса и пробелов"""
    if not re.match(r'^[А-Яа-яЁё\s-]+$', value):
        raise ValidationError(
            _('Имя может содержать только русские буквы и дефисы')
        )
    if len(value.strip()) < 2:
        raise ValidationError(
            _('Имя должно содержать минимум 2 символа')
        )

def validate_capital_first_letter(value):
    """Первая буква должна быть заглавной"""
    if value and not value[0].isupper():
        raise ValidationError(
            _('Первая буква должна быть заглавной')
        )

def validate_no_spaces(value):
    """Проверка на двойные пробелы"""
    if ' ' in value:
        raise ValidationError(
            _('Нельзя использовать пробелы')
        )

def validate_special_characters(value):
    """Запрет специальных символов"""
    forbidden_chars = r'[!@#$%^&*()_+=|<>?{}\[\]~]0123456789'
    if re.search(forbidden_chars, value):
        raise ValidationError(
            _('Имя не должно содержать специальные символы')
        )