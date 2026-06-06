# catalog/serializers.py
from rest_framework import serializers
from .models import Category, Manufacturer, Product, Cart, CartItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    item_price = serializers.ReadOnlyField()
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'item_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'total_price', 'items']
