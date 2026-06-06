# catalog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Страницы plain text из первой части (если вы их оставили)
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('author/', views.author_view, name='author'),

    # Каталог и товары из второй части
    path('catalog/', views.product_list, name='product_list'),
    path('catalog/<int:pk>/', views.product_detail, name='product_detail'),
    
    # Управление корзиной
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
