# catalog/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    country = models.CharField(max_length=100, verbose_name="Страна")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="products/", verbose_name="Фото товара")
    
    # Валидация: значение не может быть меньше 0.00
    price = models.DecimalField(
        max_length=10, 
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.00)],
        verbose_name="Цена"
    )
    
    # Валидация: значение не может быть меньше 0
    stock_quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Количество на складе"
    )
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name="products",
        verbose_name="Категория"
    )
    manufacturer = models.ForeignKey(
        Manufacturer, 
        on_delete=models.CASCADE, 
        related_name="products",
        verbose_name="Производитель"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="cart", 
        verbose_name="Пользователь"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    @property
    def total_price(self):
        """Вычисляет общую стоимость всех элементов в корзине."""
        return sum(item.item_price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name="items", 
        verbose_name="Корзина"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name="cart_items", 
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Количество"
    )

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"

    @property
    def item_price(self):
        """Возвращает стоимость элемента: цена товара * количество."""
        return self.product.price * self.quantity

    def clean(self):
        """Валидация: количество товара не должно превышать его остаток на складе."""
        super().clean()
        if self.product and self.quantity > self.product.stock_quantity:
            raise ValidationError({
                'quantity': f"Невозможно добавить {self.quantity} шт. На складе осталось всего {self.product.stock_quantity} шт."
            })

    def save(self, *args, **kwargs):
        """Вызов полной валидации перед сохранением в базу данных."""
        self.full_clean()
        super().save(*args, **kwargs)
