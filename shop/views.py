from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Item, Review, ItemInCart, ItemInOrder, Order
from .forms import AddReview
from .utils import get_sid, get_categories, get_cart
from django.core.paginator import Paginator
from django.http import HttpResponseNotAllowed


def index(request):
    smartphones = Item.objects.filter(category_id=3).select_related('category')[:3]
    clothes = Item.objects.filter(category_id=4).select_related('category')[:3]
    context = {
        'smartphones': smartphones,
        'clothes': clothes,
        'categories': get_categories(),
    }
    return render(request, 'shop/index.html', context=context)


def category(request, id):

    page = request.GET.get('page')
    page = 1 if not page else int(page)

    posts = Item.objects.filter(category_id=id).select_related('category')

    try:
        cat = posts[0].category
    except IndexError:
        cat = Category.objects.get(id=id)

    paginator = Paginator(posts, 2)

    if page > paginator.num_pages:
        page = 1

    context = {
        'categories': get_categories(),
        'items': paginator.page(page),
        'cat_name': cat.title,
    }

    return render(request, 'shop/category.html', context=context)


def item_detail(request, id):
    context = {
        'forms': AddReview(),
        'categories': get_categories(),
        'item': get_object_or_404(Item, id=id),
    }
    return render(request, 'shop/item_detail.html', context=context)


def cart_view(request):
    cart = get_cart(get_sid(request))

    context = {
        'categories': get_categories(),
        'cart': ItemInCart.objects.filter(cart=cart).select_related('item'),
    }
    return render(request, 'shop/cart.html', context=context)


def add_review(request, item_id):
    form = AddReview(request.POST)
    if form.is_valid():
        Review.objects.create(name=form.cleaned_data['name'], text=form.cleaned_data['text'],
                              star=form.cleaned_data['star'], item=Item.objects.get(id=item_id))
    return redirect('item', id=item_id)


def to_cart(request, item_id):
    if request.method == 'POST':
        cart = get_cart(get_sid(request))
        item = Item.objects.get(id=item_id)

        item_in_cart = ItemInCart.objects.filter(cart=cart, item=item).first()

        if item_in_cart:
            item_in_cart.count += 1
            item_in_cart.save()
        else:
            ItemInCart.objects.create(cart=cart, item=item, count=1)
    else:
        raise HttpResponseNotAllowed(['POST'])
    return redirect(cart_view)


def create_order(request):
    if request.method == 'POST':
        cart = get_cart(get_sid(request))
        items = cart.items.all()

        if items:
            order = Order.objects.create(owner=get_sid(request))
            for item in items:
                iib = ItemInCart.objects.get(item=item, cart=cart)
                ItemInOrder.objects.create(item=item, order=order, count=iib.count)
                iib.delete()
    else:
        raise HttpResponseNotAllowed(['POST'])
    return redirect('index')







