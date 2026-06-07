from django.core.management.base import BaseCommand
from catalog.models import Category, Manufacturer, Product, Profile
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Добавляет тестовые данные для интернет-магазина'

    def handle(self, *args, **kwargs):
        # Создаем категории
        categories = {
            'Смартфоны': 'Мобильные телефоны и смартфоны',
            'Наушники': 'Беспроводные и проводные наушники',
            'Умные часы': 'Смарт-часы и фитнес-браслеты',
            'Планшеты': 'Планшеты и электронные книги',
            'Аксессуары': 'Чехлы, защитные стекла и другие аксессуары',
        }
        
        category_objs = {}
        for name, desc in categories.items():
            obj, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
            category_objs[name] = obj
            self.stdout.write(f'Создана категория: {name}')
        
        # Создаем производителей
        manufacturers_data = [
            {'name': 'Xiaomi', 'country': 'Китай'},
            {'name': 'Samsung', 'country': 'Южная Корея'},
            {'name': 'Apple', 'country': 'США'},
            {'name': 'Huawei', 'country': 'Китай'},
            {'name': 'Sony', 'country': 'Япония'},
            {'name': 'JBL', 'country': 'США'},
            {'name': 'BelBrand', 'country': 'Беларусь'},
        ]
        
        manufacturer_objs = {}
        for m_data in manufacturers_data:
            obj, created = Manufacturer.objects.get_or_create(
                name=m_data['name'],
                defaults={'country': m_data['country']}
            )
            manufacturer_objs[obj.name] = obj
            self.stdout.write(f'Создан производитель: {obj.name}')
        
        # Создаем товары
        products_data = [
            {
                'name': 'Xiaomi Redmi Note 13',
                'description': 'Смартфон с 108MP камерой и AMOLED дисплеем. 8GB RAM, 256GB памяти.',
                'price': 1299.00,
                'stock_quantity': 15,
                'category': 'Смартфоны',
                'manufacturer': 'Xiaomi',
                'is_new': True,
            },
            {
                'name': 'Samsung Galaxy S24',
                'description': 'Флагманский смартфон с AI функциями. 12GB RAM, 512GB памяти.',
                'price': 3599.00,
                'stock_quantity': 8,
                'category': 'Смартфоны',
                'manufacturer': 'Samsung',
                'is_new': True,
            },
            {
                'name': 'Apple AirPods Pro 2',
                'description': 'Беспроводные наушники с активным шумоподавлением. Время работы до 6 часов.',
                'price': 899.00,
                'stock_quantity': 12,
                'category': 'Наушники',
                'manufacturer': 'Apple',
                'is_new': True,
            },
            {
                'name': 'Xiaomi Watch S3',
                'description': 'Умные часы с AMOLED экраном 1.43 дюйма, GPS, мониторинг здоровья.',
                'price': 399.00,
                'stock_quantity': 20,
                'category': 'Умные часы',
                'manufacturer': 'Xiaomi',
                'is_new': False,
            },
            {
                'name': 'Huawei FreeBuds Pro 3',
                'description': 'TWS наушники с шумоподавлением до 45dB. Поддержка LDAC.',
                'price': 649.00,
                'stock_quantity': 10,
                'category': 'Наушники',
                'manufacturer': 'Huawei',
                'is_new': True,
            },
            {
                'name': 'Samsung Galaxy Tab S9',
                'description': 'Мощный планшет с S Pen в комплекте. 12GB RAM, 256GB памяти.',
                'price': 2499.00,
                'stock_quantity': 5,
                'category': 'Планшеты',
                'manufacturer': 'Samsung',
                'is_new': True,
            },
            {
                'name': 'Sony WH-1000XM5',
                'description': 'Премиальные наушники с лучшим шумоподавлением. 30 часов работы.',
                'price': 1299.00,
                'stock_quantity': 7,
                'category': 'Наушники',
                'manufacturer': 'Sony',
                'is_new': False,
            },
            {
                'name': 'Xiaomi Pad 6',
                'description': 'Планшет для учебы и развлечений. 8GB RAM, 128GB памяти.',
                'price': 1099.00,
                'stock_quantity': 9,
                'category': 'Планшеты',
                'manufacturer': 'Xiaomi',
                'is_new': False,
            },
            {
                'name': 'JBL Charge 5',
                'description': 'Портативная колонка с мощным звуком. Защита от воды IP67.',
                'price': 499.00,
                'stock_quantity': 15,
                'category': 'Аксессуары',
                'manufacturer': 'JBL',
                'is_new': True,
            },
            {
                'name': 'BelBrand Часы X1',
                'description': 'Белорусские умные часы с пульсометром. Аккумулятор на 14 дней.',
                'price': 199.00,
                'stock_quantity': 30,
                'category': 'Умные часы',
                'manufacturer': 'BelBrand',
                'is_new': True,
            },
            {
                'name': 'Защитное стекло iPhone 15 Pro',
                'description': 'Прочное защитное стекло 9H. Олеофобное покрытие.',
                'price': 29.00,
                'stock_quantity': 50,
                'category': 'Аксессуары',
                'manufacturer': 'BelBrand',
                'is_new': False,
            },
            {
                'name': 'Беспроводная зарядка 15W',
                'description': 'Быстрая беспроводная зарядка для всех устройств. Совместима с Qi.',
                'price': 79.00,
                'stock_quantity': 25,
                'category': 'Аксессуары',
                'manufacturer': 'Xiaomi',
                'is_new': True,
            },
        ]
        
        for p_data in products_data:
            product, created = Product.objects.get_or_create(
                name=p_data['name'],
                defaults={
                    'description': p_data['description'],
                    'price': p_data['price'],
                    'stock_quantity': p_data['stock_quantity'],
                    'category': category_objs[p_data['category']],
                    'manufacturer': manufacturer_objs[p_data['manufacturer']],
                    'is_new': p_data['is_new'],
                }
            )
            self.stdout.write(f'{"Создан" if created else "Найден"} товар: {product.name} ({product.price} Br)')
        
        # Создаем тестового пользователя (если нет)
        if not User.objects.filter(username='user1').exists():
            user = User.objects.create_user(
                username='user1',
                email='user1@example.com',
                password='user123456'
            )
            self.stdout.write('Создан тестовый пользователь: user1 / user123456')
        
        self.stdout.write(self.style.SUCCESS('✅ Тестовые данные успешно добавлены!'))