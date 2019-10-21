from django.core.cache import cache
from .models import Category, Cart


def get_sid(request):
    if not request.user.is_authenticated:
        sid = request.session.session_key
        if not sid:
            sid = request.session.cycle_key()
    else:
        sid = request.user.username
    return sid


def get_categories():
    categories = cache.get_or_set('categories', Category.objects.filter(is_main=True).prefetch_related('sub_categories'), 3600)
    return categories


def get_cart(sid):
    cart, created = Cart.objects.get_or_create(sid=sid)
    return cart
