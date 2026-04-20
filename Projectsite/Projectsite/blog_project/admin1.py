from functools import update_wrapper

from django.http import Http404
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# Некоторые файлы не используются, например этот создался при 
#создании проекта ,в которых тоже ничего нет также создавались при созд. проекта

def admin_view(view, cacheable=False):
    """
    Overwrite the default admin view to return 404 for not logged in users.
    """
    def inner(request, *args, **kwargs):
        if not request.user.is_active and not request.user.is_staff:
            raise Http404()
        return view(request, *args, **kwargs)

    if not cacheable:
        inner = never_cache(inner)

    # We add csrf_protect here so this function can be used as a utility
    # function for any view, without having to repeat 'csrf_protect'.
    if not getattr(view, 'csrf_exempt', False):
        inner = csrf_protect(inner)

    return update_wrapper(inner, view)