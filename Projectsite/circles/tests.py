import logging
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from circles.models import Circle
from django.utils.text import slugify

User = get_user_model()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def custom_slugify(value):
    value_str = str(value)

    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
        'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    }

    transliterated_chars = [translit_dict.get(ch, ch) for ch in value_str]
    
    result = ''.join(transliterated_chars)
    return slugify(result)


class CircleModelTest(TestCase):
    def setUp(self):
        self.circle = Circle.objects.create(
            name='Робототехника, старшая группа',
            icon='fas fa-robot',
            grade='5-11 классы',
            room='9',
            teacher='Малышева И.А.',
            schedule=[
                {'day': 'monday', 'time': '15:50-17:30'},
                {'day': 'friday', 'time': '15:50-17:30'}
            ],
            days='monday,friday',
            order=1,
            is_active=True
        )
        logger.info(f"Создан кружок: {self.circle.name}")

    def test_str(self):
        self.assertEqual(str(self.circle), 'Робототехника, старшая группа')
        logger.info("__str__ работает")

    def test_slug_auto_creation(self):
        expected = custom_slugify(self.circle.name)
        self.assertEqual(self.circle.slug, expected)
        logger.info(f"Slug создан: {expected}")

    def test_slug_uniqueness(self):
        circle2 = Circle.objects.create(
            name='Робототехника, старшая группа',
            grade='1-4',
            room='1',
            teacher='A'
        )
        self.assertNotEqual(circle2.slug, self.circle.slug)
        logger.info("Уникальность slug обеспечена")

    def test_get_days_list(self):
        self.assertEqual(self.circle.get_days_list(), ['monday', 'friday'])
        logger.info("get_days_list OK")

    def test_get_schedule_display(self):
        display = self.circle.get_schedule_display()
        self.assertIn('Понедельник 15:50-17:30', display)
        self.assertIn('Пятница 15:50-17:30', display)
        logger.info("Расписание корректно")

    def test_empty_schedule(self):
        circle = Circle.objects.create(name='Новый кружок', grade='5', room='1', teacher='A')
        self.assertEqual(circle.get_schedule_display(), [])
        logger.info("Пустое расписание обработано")

    def test_order_default(self):
        circle = Circle.objects.create(name='Без порядка', grade='5', room='1', teacher='A')
        self.assertEqual(circle.order, 0)
        logger.info("Порядок по умолчанию 0")


class CircleViewAccessTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='adminpass', email='a@a.com')
        self.user = User.objects.create_user(username='user', password='userpass', email='u@u.com')
        self.circle = Circle.objects.create(name='Тестовый кружок', grade='5', room='1', teacher='A')
        logger.info("Тестовые данные доступа созданы")

    def test_anonymous_cannot_create_circle(self):
        response = self.client.get(reverse('circles:circle_create'))
        self.assertEqual(response.status_code, 302)
        logger.info("Аноним не может создать кружок")

    def test_user_cannot_create_circle(self):
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('circles:circle_create'))
        self.assertEqual(response.status_code, 302)
        logger.info("Обычный пользователь не может создать кружок")

    def test_admin_can_create_circle(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('circles:circle_create'))
        self.assertEqual(response.status_code, 200)
        logger.info("Администратор может создать кружок")

    def test_anonymous_cannot_edit_circle(self):
        response = self.client.get(reverse('circles:circle_edit', args=[self.circle.slug]))
        self.assertEqual(response.status_code, 302)
        logger.info("Аноним не может редактировать кружок")

    def test_user_cannot_edit_circle(self):
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('circles:circle_edit', args=[self.circle.slug]))
        self.assertEqual(response.status_code, 302)
        logger.info("Обычный пользователь не может редактировать кружок")

    def test_admin_can_edit_circle(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('circles:circle_edit', args=[self.circle.slug]))
        self.assertEqual(response.status_code, 200)
        logger.info("Администратор может редактировать кружок")