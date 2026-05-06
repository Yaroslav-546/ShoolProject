import logging
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from students.models import Profile
from circles.models import Circle

User = get_user_model()
logger = logging.getLogger(__name__)


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='student', email='student@ex.com', password='pass',
            first_name='Ученик', last_name='Тестов'
        )
        self.circle_name = 'Робототехника, старшая группа'
        Circle.objects.get_or_create(
            name=self.circle_name,
            defaults={'grade': '5-11', 'room': '9', 'teacher': 'A'}
        )
        self.profile = Profile.objects.create(
            user=self.user,
            family=self.user.last_name,
            name=self.user.first_name,
            active=self.circle_name,
            Class='10А'
        )
        logger.info(f"Создан профиль для пользователя {self.user.username}")

    def test_str(self):
        expected = f"{self.user.last_name} {self.user.first_name}, {self.circle_name}"
        self.assertEqual(str(self.profile), expected)
        logger.info("__str__ работает")

    def test_unique_together(self):
        with self.assertRaises(IntegrityError):
            Profile.objects.create(
                user=self.user,
                family=self.user.last_name,
                name=self.user.first_name,
                active=self.circle_name,
                Class='11Б'
            )
        logger.info("Уникальность пары (user, active) соблюдается")

    def test_created_at_auto(self):
        self.assertIsNotNone(self.profile.created_at)
        logger.info("created_at автоматически проставляется")

    def test_class_field_max_length(self):
        user2 = User.objects.create_user(username='student2', email='s2@ex.com', password='pass')
        circle2 = Circle.objects.create(name='Другой кружок', grade='5-7', room='10', teacher='B')
        profile = Profile.objects.create(
            user=user2,
            family='Тест',
            name='Тест',
            active=circle2.name,
            Class='10А'
        )
        self.assertEqual(profile.Class, '10А')
        logger.info("Поле Class работает")


class ProfileViewAccessTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='adminpass', email='a@a.com')
        self.user = User.objects.create_user(username='user', password='userpass', email='u@u.com')
        self.circle = Circle.objects.create(name='Кружок', grade='5', room='1', teacher='A')
        self.profile = Profile.objects.create(
            user=self.user,
            family='Фамилия',
            name='Имя',
            active=self.circle.name,
            Class='10А'
        )
        logger.info("Тестовые данные для доступа созданы")

    def test_anonymous_cannot_view_students_list(self):
        response = self.client.get(reverse('studentslist'))
        self.assertEqual(response.status_code, 302)
        logger.info("Аноним не имеет доступа к списку учеников")

    def test_user_cannot_view_students_list(self):
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('studentslist'))
        self.assertEqual(response.status_code, 302)
        logger.info("Обычный пользователь не видит список учеников")

    def test_admin_can_view_students_list(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('studentslist'))
        self.assertEqual(response.status_code, 200)
        logger.info("Администратор видит список учеников")