import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from gallery.models import GalleryImage

class Command(BaseCommand):
    help = 'Импортирует изображения из статической папки в галерею'

    def handle(self, *args, **options):
        # Список данных из вашего предыдущего JavaScript (image, description)
        slides_data = [
            {"image": "Images/chess-1.png", "description": "Шахматы"},
            {"image": "Images/chess-2.jpg", "description": "Шахматы"},
            {"image": "Images/chess-new-gambit.jpg", "description": "Шахматы 'Новый гамбит'"},
            {"image": "Images/day-respublic.jpg", "description": "День Республики"},
            {"image": "Images/geoinform.jpg", "description": "Геоинформатика"},
            {"image": "Images/geoinform-1.jpg", "description": "Геоинформатика"},
            {"image": "Images/Night-in-museum.jpg", "description": "Ночь музеев 2021"},
            {"image": "Images/obj.jpg", "description": "ОБЖ"},
            {"image": "Images/obj-1.jpg", "description": "ОБЖ"},
            {"image": "Images/program-1.jpg", "description": "Программирование"},
            {"image": "Images/promdis.jpg", "description": "Промышленный дизайн"},
            {"image": "Images/promdis-1.jpg", "description": "Промышленный дизайн"},
            {"image": "Images/votocnimok-jpg.jpg", "description": "Фотосъемка"},
            {"image": "Images/votocnimok-jpg-1.jpg", "description": "Фотосъемка"},
            {"image": "Images/vr.jpg", "description": "Виртуальная реальность"},
            {"image": "Images/vr-1.jpg", "description": "Виртуальная реальность"},
            {"image": "Images/program.png", "description": "Программирование"},
            {"image": "Images/robotics-1.png", "description": "Робототехника"},
            {"image": "Images/robotics-2.png", "description": "Робототехника"},
            {"image": "Images/volonter.jpg", "description": "Волонтерство"},
            {"image": "Images/giber.jpg", "description": "Соревнования по Берлоге"},
            {"image": "Images/win-fast-chess.jpg", "description": "Шахматы"},
            {"image": "Images/new-resurs.jpg", "description": "Новое оборудование"},
            {"image": "Images/win-day-resp.jpg", "description": "Шахматы"},
            {"image": "Images/win-white.jpg", "description": "Шахматы"},
        ]

        base_dir = settings.BASE_DIR
        static_dir = os.path.join(base_dir, 'static')
        # Или media_dir = os.path.join(base_dir, 'media/gallery')

        for item in slides_data:
            image_path = os.path.join(static_dir, item['image'])
            if not os.path.exists(image_path):
                self.stdout.write(self.style.WARNING(f'Файл не найден: {item["image"]}'))
                continue

            # Открываем файл и создаём запись в БД
            with open(image_path, 'rb') as f:
                # Сохраняем файл в поле image модели (upload_to='gallery/')
                # Для этого нужно скопировать файл в media/gallery/
                # Проще: использовать Django File
                from django.core.files.images import ImageFile
                image_file = ImageFile(f, name=os.path.basename(item['image']))
                gallery_item = GalleryImage(
                    title=item['description'],
                    description=item['description'],
                    order=0,
                    is_active=True
                )
                gallery_item.image.save(image_file.name, image_file, save=True)
                self.stdout.write(self.style.SUCCESS(f'Добавлено: {item["image"]}'))

        self.stdout.write(self.style.SUCCESS('Импорт завершён.'))