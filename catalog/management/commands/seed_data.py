# catalog/management/commands/seed_data.py
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from catalog.models import Category, Manufacturer, Product, Cart, CartItem

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        self.stdout.write('Удаление старых данных...')
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Manufacturer.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # 1. Создание 5 производителей
        self.stdout.write('Создание производителей...')
        manufacturers_data = [
            {"name": "Xiaomi", "country": "Китай"},
            {"name": "Apple", "country": "США"},
            {"name": "Samsung", "country": "Южная Корея"},
            {"name": "JBL", "country": "США"},
            {"name": "Huawei", "country": "Китай"},
        ]
        manufacturers = [Manufacturer.objects.create(**m) for m in manufacturers_data]

        # 2. Создание 10 категорий портативных гаджетов
        self.stdout.write('Создание категорий...')
        categories_titles = [
            "Умные часы", "Беспроводные наушники", "Портативные колонки", 
            "Внешние аккумуляторы", "Автомобильные гаджеты", "Экшн-камеры", 
            "Электронные книги", "Умный дом", "Беспроводные зарядки", "Фитнес-браслеты"
        ]
        categories = [Category.objects.create(name=name, description=f"Каталог товаров из категории: {name}") for name in categories_titles]

        # 3. Создание 34 товаров
        self.stdout.write('Создание товаров...')
        products = []
        for i in range(1, 35):
            category = random.choice(categories)
            manufacturer = random.choice(manufacturers)
            product = Product.objects.create(
                name=f"Гаджет {manufacturer.name} Model-{i}",
                description=f"Инновационный портативный девайс от бренда {manufacturer.name}. Отличный выбор в категории {category.name}.",
                price=round(random.uniform(25.00, 1500.00), 2),
                stock_quantity=random.randint(10, 50),
                category=category,
                manufacturer=manufacturer,
                image="products/default.jpg" # Файл-заглушка
            )
            products.append(product)

        # 4. Создание 5 пользователей и их корзин
        self.stdout.write('Создание пользователей и корзин...')
        for i in range(1, 6):
            username = f"user_{i}"
            user = User.objects.create_user(username=username, password="password123")
            
            # Django автоматически создает или мы вручную привязываем корзину
            cart = Cart.objects.create(user=user)
            
            # Добавляем по 2-3 случайных товара в корзину каждого пользователя
            selected_products = random.sample(products, k=random.randint(2, 3))
            for product in selected_products:
                CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=random.randint(1, 3) # На складе точно хватит (там от 10 шт)
                )

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))
