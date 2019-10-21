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
    categories = cache.get_or_set('categories', Category.objects.filter(is_main=True), 3600)
    # Задебажив запрос - убрал все лишнее в функции
    # SELECT shop_category.id, shop_category.title, shop_category.is_main, shop_category.main_category_id
    # FROM shop_category
    # WHERE shop_category.is_main = True
    # ORDER BY shop_category.id ASC
    return categories


def get_cart(sid):
    cart, created = Cart.objects.get_or_create(sid=sid)
    return cart
