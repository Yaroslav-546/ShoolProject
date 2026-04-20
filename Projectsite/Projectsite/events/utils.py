from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_registration_email(user, event, registration):
    """
    Отправка письма при успешной регистрации на мероприятие
    """
    subject = f'Подтверждение регистрации на мероприятие "{event.title}"'

    # HTML контекст для письма
    context = {
        'user': user,
        'event': event,
        'registration': registration,
        'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else '',
    }

    # HTML версия письма
    html_message = render_to_string('registration_confirmation.html', context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
        html_message=html_message
    )


def send_cancellation_email(user, event, registration):
    """
    Отправка письма при отмене регистрации
    """
    subject = f'Отмена регистрации на мероприятие "{event.title}"'

    context = {
        'user': user,
        'event': event,
        'registration': registration,
    }

    html_message = render_to_string('registration_cancelled.html', context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
        html_message=html_message
    )


def send_waiting_list_email(user, event, registration):
    """
    Отправка письма при добавлении в лист ожидания
    """
    subject = f'Вы добавлены в лист ожидания на мероприятие "{event.title}"'

    context = {
        'user': user,
        'event': event,
        'registration': registration,
    }

    html_message = render_to_string('waiting_list.html', context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
        html_message=html_message
    )


def send_confirmation_from_waiting_email(user, event, registration):
    """
    Отправка письма при подтверждении из листа ожидания
    """
    subject = f'Ваша регистрация на мероприятие "{event.title}" подтверждена!'

    context = {
        'user': user,
        'event': event,
        'registration': registration,
    }

    html_message = render_to_string('confirmed_from_waiting.html', context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
        html_message=html_message
    )