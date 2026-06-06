# catalog/admin.py
from django.contrib import admin
from .models import Category, Manufacturer, Product, Cart, CartItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    search_fields = ('name', 'country')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'manufacturer', 'price', 'stock_quantity')
    list_filter = ('category', 'manufacturer')
    search_fields = ('name', 'description')

class CartItemInline(admin.TabularInline):
    """Позволяет редактировать элементы корзины прямо внутри страницы самой корзины."""
    model = CartItem
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'get_total_price')
    search_fields = ('user__username',)
    inlines = [CartItemInline]

    def get_total_price(self, obj):
        return f"{obj.total_price:.2f} руб."
    get_total_price.short_description = "Общая стоимость"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'get_item_price')
    list_filter = ('cart__user',)
    
    def get_item_price(self, obj):
        return f"{obj.item_price:.2f} руб."
    get_item_price.short_description = "Стоимость элемента"
