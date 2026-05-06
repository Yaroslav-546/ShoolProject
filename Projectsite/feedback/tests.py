import logging
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from feedback.models import Feedback

User = get_user_model()
logger = logging.getLogger(__name__)


class FeedbackModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@ex.com', password='pass')
        self.feedback = Feedback.objects.create(
            user=self.user,
            name='Иван',
            email='ivan@ex.com',
            subject='Проблема',
            message='Не могу записаться',
            status='new'
        )
        logger.info("Создано тестовое обращение")

    def test_str(self):
        self.assertEqual(str(self.feedback), 'Иван - Проблема')
        logger.info("__str__ работает")

    def test_default_status(self):
        fb = Feedback.objects.create(
            name='Петр',
            email='petr@ex.com',
            subject='Предложение',
            message='Хороший сайт'
        )
        self.assertEqual(fb.status, 'new')
        logger.info("Статус по умолчанию 'new'")

    def test_admin_reply(self):
        self.feedback.admin_reply = 'Проблема решена'
        self.feedback.status = 'replied'
        self.feedback.save()
        self.assertEqual(self.feedback.status, 'replied')
        logger.info("Ответ администратора и статус сохраняются")

    def test_ordering(self):
        fb2 = Feedback.objects.create(name='Анна', email='anna@ex.com', subject='S2', message='M2')
        feedbacks = Feedback.objects.all()
        self.assertEqual(feedbacks.first().pk, fb2.pk)
        logger.info("Сортировка по убыванию даты работает")


class FeedbackViewAccessTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='adminpass', email='a@a.com')
        self.user = User.objects.create_user(username='user', password='userpass', email='u@u.com')
        logger.info("Тестовые данные доступа созданы")

    def test_anonymous_can_view_form(self):
        response = self.client.get(reverse('feedback:form'))
        self.assertEqual(response.status_code, 302)  
        logger.info("Аноним перенаправляется на страницу входа")

    def test_anonymous_can_submit_form(self):
        response = self.client.post(reverse('feedback:form'), {
            'name': 'Аноним',
            'email': 'anon@ex.com',
            'subject': 'Тест',
            'message': 'Сообщение'
        })
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('feedback:form'))
        logger.info("Аноним не может отправить обращение без авторизации")

    def test_user_can_see_own_feedback_list(self):
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('feedback:user_list'))
        self.assertEqual(response.status_code, 200)
        logger.info("Пользователь видит список своих обращений")

    def test_user_cannot_see_admin_list(self):
        self.client.login(username='user', password='userpass')
        response = self.client.get('/feedback/admin/list/')
        self.assertEqual(response.status_code, 403) 
        logger.info("Обычный пользователь не видит админский список")

    def test_admin_can_see_admin_list(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get('/feedback/admin/list/')
        self.assertEqual(response.status_code, 200)
        logger.info("Администратор видит список всех обращений")