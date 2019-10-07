from django.urls import path
from shop import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('category/<id>/', views.category, name='category'),
    path('item/<id>/', views.item_detail, name='item'),
    path('item/<item_id>/add_review/', views.add_review, name='add_review'),
    path('item/<item_id>/to_cart/', views.to_cart, name='to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create_order/', views.create_order, name='create_order')
]


