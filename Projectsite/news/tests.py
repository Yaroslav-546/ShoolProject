# news/tests.py
import logging
import tempfile
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from news.models import News

User = get_user_model()
logger = logging.getLogger(__name__)

# Утилита для создания временного изображения
def get_temp_image():
    image = Image.new('RGB', (100, 100), color='red')
    tmp = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp, 'jpeg')
    tmp.seek(0)
    return SimpleUploadedFile(tmp.name, tmp.read(), content_type='image/jpeg')


# ========== ТЕСТЫ МОДЕЛИ ==========
class NewsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.image = get_temp_image()
        cls.news = News.objects.create(
            title='Тестовая новость',
            body='Содержание новости',
            image=cls.image
        )
        logger.info(f"Создана тестовая новость: {cls.news.title}")

    def test_str_method(self):
        self.assertEqual(str(self.news), 'Тестовая новость')
        logger.info("Проверка __str__: успешно")

    def test_get_absolute_url(self):
        url = self.news.get_absolute_url()
        self.assertEqual(url, f'/post/{self.news.id}/')
        logger.info(f"get_absolute_url возвращает {url}")

    def test_ordering(self):
        news2 = News.objects.create(
            title='Более новая',
            body='text',
            image=get_temp_image()
        )
        self.assertGreater(news2.date, self.news.date)
        latest = News.objects.first()
        self.assertEqual(latest.title, 'Более новая')
        logger.info("Сортировка по убыванию даты работает")

    def test_title_max_length(self):
        long_title = 'А' * 250  # больше max_length=200
        news = News(
            title=long_title,
            body='text',
            image=get_temp_image()
        )
        with self.assertRaises(ValidationError):
            news.full_clean()
        logger.info("Ожидаемая ошибка валидации длины заголовка возникла")

    # Так как поле image не обязательно, тест проверяет возможность создания без картинки
    def test_image_optional(self):
        news = News.objects.create(
            title='Без картинки',
            body='text',
            image=None
        )
        self.assertIsNotNone(news)
        logger.info("Поле image не обязательно – создание без файла допустимо")


# ========== ТЕСТЫ ПРЕДСТАВЛЕНИЙ ==========
class NewsViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.image = get_temp_image()
        cls.news = News.objects.create(
            title='Новость для списка',
            body='Текст',
            image=cls.image
        )
        cls.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass',
            email='admin@ex.com'
        )
        cls.user = User.objects.create_user(
            username='user',
            password='userpass',
            email='user@ex.com'
        )
        logger.info("Тестовые данные созданы")

    def test_news_list_view(self):
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.news.title)
        logger.info("Страница списка новостей доступна")

    def test_news_detail_view(self):
        response = self.client.get(reverse('post_detail', args=[self.news.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.news.title)
        logger.info("Страница деталей новости доступна")

    def test_create_news_by_anonymous(self):
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 302)  # редирект на логин
        logger.info("Анонимный пользователь не имеет доступа к созданию")

    def test_create_news_by_admin(self):
        self.client.login(username='admin', password='adminpass')
        image = get_temp_image()
        response = self.client.post(reverse('post_new'), {
            'title': 'Новая новость от админа',
            'body': 'Содержание',
            'image': image,
        })
        self.assertEqual(response.status_code, 302)  # редирект после успеха
        self.assertTrue(News.objects.filter(title='Новая новость от админа').exists())
        logger.info("Админ создал новость")

    def test_create_news_by_user(self):
        self.client.login(username='user', password='userpass')
        image = get_temp_image()
        response = self.client.post(reverse('post_new'), {
            'title': 'Новость от пользователя',
            'body': 'Текст',
            'image': image,
        })
        # Пользователь перенаправляется на страницу ошибки 403
        self.assertRedirects(response, reverse('error403'))
        self.assertFalse(News.objects.filter(title='Новость от пользователя').exists())
        logger.info("Обычный пользователь не может создать новость")

    def test_update_news_by_admin(self):
        self.client.login(username='admin', password='adminpass')
        image = get_temp_image()
        response = self.client.post(reverse('post_edit', args=[self.news.id]), {
            'title': 'Обновлённый заголовок',
            'body': 'Новый текст',
            'image': image,
        })
        self.assertEqual(response.status_code, 302)
        self.news.refresh_from_db()
        self.assertEqual(self.news.title, 'Обновлённый заголовок')
        logger.info("Админ обновил новость")

    def test_update_news_by_user(self):
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('post_edit', args=[self.news.id]))
        self.assertRedirects(response, reverse('error403'))
        logger.info("Обычный пользователь не может редактировать новость")

    def test_delete_news_by_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('post_delete', args=[self.news.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(News.objects.filter(id=self.news.id).exists())
        logger.info("Админ удалил новость")

    def test_delete_news_by_user(self):
        self.client.login(username='user', password='userpass')
        response = self.client.post(reverse('post_delete', args=[self.news.id]))
        self.assertRedirects(response, reverse('error403'))
        logger.info("Обычный пользователь не может удалить новость")


# ========== ТЕСТЫ КРАЕВЫХ СЛУЧАЕВ ==========
class NewsEdgeCasesTest(TestCase):

    def test_very_long_title(self):
        long_title = 'А' * 250
        news = News(
            title=long_title,
            body='text',
            image=get_temp_image()
        )
        with self.assertRaises(ValidationError):
            news.full_clean()
        logger.info("Тест: очень длинный заголовок (более 200 символов)")

    def test_empty_body(self):
        news = News.objects.create(
            title='Пустое тело',
            body='',
            image=get_temp_image()
        )
        self.assertEqual(news.body, '')
        logger.info("Пустое тело допустимо")