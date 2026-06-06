# catalog/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Создаем роутер и регистрируем ViewSets
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='api-category')
router.register(r'manufacturers', views.ManufacturerViewSet, basename='api-manufacturer')
router.register(r'products', views.ProductViewSet, basename='api-product')
router.register(r'carts', views.CartViewSet, basename='api-cart')
router.register(r'cart-items', views.CartItemViewSet, basename='api-cartitem')

urlpatterns = [
    # Ваши HTML-маршруты из прошлых заданий
    path('', views.home_view, name='home'),
    path('catalog/', views.product_list, name='product_list'),
    path('catalog/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),

    # Подключение автоматических маршрутов API (будет работать как /api/products/ и т.д.)
    path('api/', include(router.urls)),
]
