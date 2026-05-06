import logging
import tempfile
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from gallery.models import GalleryImage

logger = logging.getLogger(__name__)


def get_temp_image():
    image = Image.new('RGB', (100, 100), color='red')
    tmp = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp, 'jpeg')
    tmp.seek(0)
    return SimpleUploadedFile(tmp.name, tmp.read(), content_type='image/jpeg')


class GalleryImageTest(TestCase):
    def setUp(self):
        self.image = GalleryImage.objects.create(
            title='Тестовое изображение',
            image=get_temp_image(),
            description='Описание',
            order=1,
            is_active=True
        )
        logger.info("Создано тестовое изображение для галереи")

    def test_str(self):
        self.assertEqual(str(self.image), 'Тестовое изображение')
        logger.info("__str__ работает")

    def test_default_order(self):
        img2 = GalleryImage.objects.create(
            title='Без порядка',
            image=get_temp_image()
        )
        self.assertEqual(img2.order, 0)
        logger.info("Поле order по умолчанию 0")

    def test_active_filter(self):
        img2 = GalleryImage.objects.create(
            title='Неактивно',
            image=get_temp_image(),
            is_active=False
        )
        self.assertEqual(GalleryImage.objects.filter(is_active=True).count(), 1)
        self.assertEqual(GalleryImage.objects.filter(is_active=False).count(), 1)
        logger.info("Фильтрация по is_active работает")