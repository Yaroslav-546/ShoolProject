import logging
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from unittest.mock import patch
from datetime import timedelta
from django.utils import timezone

User = get_user_model()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович',
            grade='10А'
        )
        logger.info(f"Создан тестовый пользователь: {self.user.username}")

    def test_create_user(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpass123'))
        logger.info("Тест создания пользователя пройден")

    def test_full_name(self):
        self.assertEqual(self.user.get_full_name(), 'Иванов Иван Иванович')
        logger.info("Метод get_full_name работает")

    def test_validation_russian_name(self):
        user = User(username='bad', email='bad@ex.com', password='pass',
                    first_name='John', last_name='Doe')
        with self.assertRaises(ValidationError):
            user.full_clean()
        logger.info("Валидация имени (только русские буквы) работает")

    def test_capital_first_letter(self):
        user = User(username='test2', email='t2@ex.com', password='pass',
                    first_name='иван', last_name='петров')
        with self.assertRaises(ValidationError):
            user.full_clean()
        logger.info("Валидация заглавной первой буквы работает")

    def test_no_spaces(self):
        user = User(username='test3', email='t3@ex.com', password='pass',
                    first_name='Иван Иванов')
        with self.assertRaises(ValidationError):
            user.full_clean()
        logger.info("Валидация отсутствия пробелов работает")

    @patch('accounts.models.send_mail')
    @override_settings(EMAIL_HOST_USER='test@example.com')
    def test_send_verification_email(self, mock_send_mail):
        request = type('Request', (), {'build_absolute_uri': lambda self, path: f'http://test.com{path}'})()
        self.user.send_verification_email(request)
        mock_send_mail.assert_called_once()
        args = mock_send_mail.call_args[0]
        self.assertIn('Подтверждение электронной почты', args[0])
        self.assertEqual(args[3][0], self.user.email)
        logger.info("Письмо подтверждения отправляется")

    def test_generate_password_reset_token(self):
        token = self.user.generate_password_reset_token()
        self.assertIsNotNone(token)
        self.assertAlmostEqual(self.user.reset_password_expires,
                               timezone.now() + timedelta(hours=24), delta=timedelta(seconds=2))
        logger.info("Токен сброса пароля генерируется")

    def test_is_password_reset_token_valid(self):
        self.user.generate_password_reset_token()
        self.assertTrue(self.user.is_password_reset_token_valid())
        self.user.reset_password_expires = timezone.now() - timedelta(hours=1)
        self.assertFalse(self.user.is_password_reset_token_valid())
        logger.info("Проверка валидности токена работает")

    def test_clear_password_reset_token(self):
        self.user.generate_password_reset_token()
        self.user.clear_password_reset_token()
        self.assertIsNone(self.user.reset_password_token)
        self.assertIsNone(self.user.reset_password_expires)
        logger.info("Очистка токена работает")


class UserAccessTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='adminpass', email='admin@ex.com')
        self.user = User.objects.create_user(username='user', password='userpass', email='user@ex.com')
        logger.info("Созданы пользователи для теста доступа")

    def test_admin_can_access_admin_panel(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        logger.info("Администратор имеет доступ к админке")

    def test_anonymous_cannot_access_admin_panel(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 403)
        logger.info("Аноним перенаправлен на страницу входа")

    def test_user_cannot_access_admin_panel(self):
        self.client.login(username='user', password='userpass')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 403)
        logger.info("Обычный пользователь не имеет доступа к админке (403)")

class PasswordResetIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='resetuser',
            email='reset@example.com',
            password='oldpass123',
            first_name='Сброс',
            last_name='Тестов'
        )

    def test_reset_page_accessible(self):
        response = self.client.get(reverse('password-reset'))
        self.assertEqual(response.status_code, 200)

    @patch('accounts.models.send_mail')
    def test_reset_request_sends_email(self, mock_send_mail):
        response = self.client.post(reverse('password-reset'), {'email': self.user.email})
        self.assertEqual(response.status_code, 302)
        mock_send_mail.assert_called_once()
        args = mock_send_mail.call_args[0]
        self.assertIn('Сброс пароля', args[0])
        self.assertEqual(args[3][0], self.user.email)

    def test_full_reset_flow(self):
        response = self.client.post(reverse('password-reset'), {'email': self.user.email})
        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        token = self.user.reset_password_token
        logger.info(f"Сгенерирован токен: {token}")
        self.assertIsNotNone(token)

        response = self.client.get(reverse('password-reset-confirm', kwargs={'token': token}))
        self.assertEqual(response.status_code, 200)

        new_password = 'NewPass456!'
        response = self.client.post(
            reverse('password-reset-confirm', kwargs={'token': token}),
            {'new_password1': new_password, 'new_password2': new_password}
        )
        self.assertRedirects(response, reverse('password-reset-complete'))

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))
        self.assertIsNone(self.user.reset_password_token)
        self.assertIsNone(self.user.reset_password_expires)
        logger.info("Сброс пароля прошёл успешно")