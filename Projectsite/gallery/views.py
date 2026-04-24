from django.views.generic import ListView
from .models import GalleryImage

class GalleryView(ListView):
    model = GalleryImage
    template_name = 'gallery.html'
    context_object_name = 'images'
    queryset = GalleryImage.objects.filter(is_active=True).order_by('order', 'created_at')