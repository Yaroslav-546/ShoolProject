# events/tests.py
import logging
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from events.models import Event, EventRegistration
from accounts.models import CustomUser
from django.urls import reverse

logger = logging.getLogger(__name__)

class EventRegistrationFlowTest(TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        self.user1 = CustomUser.objects.create_user(username='user1', password='pass', email='u1@ex.com')
        self.user2 = CustomUser.objects.create_user(username='user2', password='pass', email='u2@ex.com')
        self.user3 = CustomUser.objects.create_user(username='user3', password='pass', email='u3@ex.com')
        
        self.event = Event.objects.create(
            title='Мероприятие с ограничением мест',
            event_type='chess',
            start_date=timezone.now() + timedelta(days=5),
            end_date=timezone.now() + timedelta(days=5, hours=2),
            registration_deadline=timezone.now() + timedelta(days=2),
            location='Зал 1',
            max_participants=2,
            current_participants=0,
            is_active=True
        )
        logger.info(f"Создано мероприятие: {self.event.title}, макс. участников: {self.event.max_participants}")

    def _register_user(self, user, expected_status):
        """Вспомогательный метод для регистрации"""
        registration = EventRegistration.objects.create(
            event=self.event,
            user=user,
            full_name=user.get_full_name() or user.username,
            grade='10А',
            email=user.email
        )
        if self.event.current_participants < self.event.max_participants:
            registration.status = 'confirmed'
            self.event.current_participants += 1
            self.event.save()
            logger.info(f"Пользователь {user.username} зарегистрирован (статус confirmed). Свободных мест: {self.event.max_participants - self.event.current_participants}")
        else:
            registration.status = 'waiting'
            logger.warning(f"Все места заняты. Пользователь {user.username} добавлен в лист ожидания (waiting).")
        registration.save()
        self.assertEqual(registration.status, expected_status)
        return registration

    def test_waiting_list_flow(self):
        logger.info("=== ТЕСТ: Заполнение мест и добавление в лист ожидания ===")
        
        reg1 = self._register_user(self.user1, 'confirmed')
        reg2 = self._register_user(self.user2, 'confirmed')
        
        reg3 = self._register_user(self.user3, 'waiting')
        logger.info(f"Позиция в листе ожидания: {EventRegistration.objects.filter(event=self.event, status='waiting').count()}")
        
        waiting_list = EventRegistration.objects.filter(event=self.event, status='waiting')
        self.assertEqual(waiting_list.count(), 1)
        self.assertEqual(waiting_list.first().user, self.user3)
        logger.info(f"Лист ожидания содержит {waiting_list.count()} пользователя(ей).")
        
        logger.info(f"Пользователь {self.user1.username} отменяет запись.")
        was_confirmed = reg1.status == 'confirmed'
        if was_confirmed:
            self.event.current_participants -= 1
            self.event.save()
        reg1.status = 'cancelled'
        reg1.save()
        logger.info(f"Свободных мест после отмены: {self.event.max_participants - self.event.current_participants}")
        
        next_waiting = EventRegistration.objects.filter(event=self.event, status='waiting').order_by('registration_date').first()
        if next_waiting and self.event.current_participants < self.event.max_participants:
            next_waiting.status = 'confirmed'
            next_waiting.save()
            self.event.current_participants += 1
            self.event.save()
            logger.info(f"Пользователь {next_waiting.user.username} перемещён из листа ожидания в confirmed.")
        
        self.assertEqual(EventRegistration.objects.filter(event=self.event, status='waiting').count(), 0)
        self.assertEqual(self.event.current_participants, self.event.max_participants)
        logger.info("=== ТЕСТ ПРОЙДЕН: Лист ожидания работает корректно ===\n")

    def test_registration_when_full(self):
        logger.info("=== ТЕСТ: Попытка записи при полном заполнении ===")
        self._register_user(self.user1, 'confirmed')
        self._register_user(self.user2, 'confirmed')
        
        reg3 = self._register_user(self.user3, 'waiting')
        self.assertEqual(reg3.status, 'waiting')
        logger.info("Третий пользователь не может записаться и помещён в waiting (ожидаемый результат).")
        
        with self.assertRaises(Exception) as context:
            EventRegistration.objects.create(
                event=self.event,
                user=self.user3,
                full_name=self.user3.get_full_name() or self.user3.username,
                grade='10А',
                email=self.user3.email
            )
        logger.info("Повторная запись того же пользователя невозможна (ограничение unique_together).")
        self.assertIn('UNIQUE constraint failed', str(context.exception))
        logger.info("=== ТЕСТ ПРОЙДЕН ===\n")

from django.contrib.auth import get_user_model
User = get_user_model()

class EventViewAccessTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='adminpass', email='a@a.com')
        self.user = User.objects.create_user(username='user', password='userpass', email='u@u.com')
        self.event = Event.objects.create(
            title='Турнир',
            event_type='chess',
            start_date=timezone.now() + timedelta(days=10),
            end_date=timezone.now() + timedelta(days=10, hours=2),
            registration_deadline=timezone.now() + timedelta(days=5),
            location='Зал',
            max_participants=10,
            is_active=True
        )
        logger.info("Тестовые данные мероприятий созданы")

    def test_anonymous_cannot_create_event(self):
        response = self.client.get(reverse('events:event_create'))
        self.assertEqual(response.status_code, 302)
        logger.info("Аноним не может создать мероприятие")


    def test_user_cannot_create_event(self):
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('events:event_create'))
        self.assertEqual(response.status_code, 403)
        logger.info("Обычный пользователь не может создать мероприятие (403)")

    def test_user_cannot_edit_event(self):
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('events:event_edit', args=[self.event.pk]))
        self.assertEqual(response.status_code, 403)
        logger.info("Обычный пользователь не может редактировать мероприятие (403)")

    def test_anonymous_cannot_edit_event(self):
        response = self.client.get(reverse('events:event_edit', args=[self.event.pk]))
        self.assertEqual(response.status_code, 302)
        logger.info("Аноним не может редактировать мероприятие")

    def test_admin_can_edit_event(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('events:event_edit', args=[self.event.pk]))
        self.assertEqual(response.status_code, 200)
        logger.info("Администратор может редактировать мероприятие")