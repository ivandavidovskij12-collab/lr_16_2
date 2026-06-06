# catalog/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views  # ДОБАВЬТЕ ЭТУ СТРОКУ
from . import views


router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='api-category')
router.register(r'manufacturers', views.ManufacturerViewSet, basename='api-manufacturer')
router.register(r'products', views.ProductViewSet, basename='api-product')
router.register(r'carts', views.CartViewSet, basename='api-cart')
router.register(r'cart-items', views.CartItemViewSet, basename='api-cartitem')

urlpatterns = [
    # Веб-страницы магазина
    path('', views.home_view, name='home'),
    path('catalog/', views.product_list, name='product_list'),  # Имя 'product_list'
    path('catalog/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    # Эндпоинты REST API
    path('api/', include(router.urls)),
]