# catalog/views.py
import io
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse                    # Для строк 99, 108, 118
from django.db.models import Q                          # Для строки 133
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Manufacturer, Cart, CartItem
from openpyxl import Workbook           # Уберет ошибку со строки 27 ("Workbook")
from django.core.mail import EmailMessage  # Уберет ошибку со строки 67 ("EmailMessage")
from django.conf import settings  
@login_required
def checkout(request):
    """Оформление заказа, генерация Excel-чека и отправка по Email."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    # Если корзина пуста, оформлять заказ нельзя
    if not cart_items:
        messages.error(request, "Ваша корзина пуста. Нечего оформлять!")
        return redirect('cart_view')

    if request.method == 'POST':
        address = request.POST.get('address', '').strip()
        if not address:
            messages.error(request, "Пожалуйста, укажите адрес доставки.")
            return render(request, 'shop/checkout.html', {'cart': cart})

        # 1. ГЕНЕРАЦИЯ ЧЕКА В ФОРМАТЕ EXCEL
        wb = Workbook()
        ws = wb.active
        ws.title = "Чек заказа"

        # Стилизация структуры таблицы чека
        ws['A1'] = f"ЧЕК ЗАКАЗА ДЛЯ ПОЛЬЗОВАТЕЛЯ: {request.user.username}"
        ws['A2'] = f"Адрес доставки: {address}"
        ws['A4'] = "Товар"
        ws['B4'] = "Цена за ед."
        ws['C4'] = "Количество"
        ws['D4'] = "Итоговая стоимость"

        row = 5
        for item in cart_items:
            ws.cell(row=row, column=1, value=item.product.name)
            ws.cell(row=row, column=2, value=float(item.product.price))
            ws.cell(row=row, column=3, value=item.quantity)
            ws.cell(row=row, column=4, value=float(item.item_price))
            row += 1

        ws.cell(row=row+1, column=3, value="ИТОГО К ОПЛАТЕ:")
        ws.cell(row=row+1, column=4, value=float(cart.total_price))

        # Сохраняем Excel-файл в буфер памяти, чтобы не засорять диск
        excel_buffer = io.BytesIO()
        wb.save(excel_buffer)
        excel_buffer.seek(0)

        # 2. ОТПРАВКА ЧЕКА ПО ЭЛЕКТРОННОЙ ПОЧТЕ
        user_email = request.user.email if request.user.email else f"{request.user.username}@example.com"
        
        subject = f"Ваш заказ в Portative Shop успешно оформлен!"
        body = (
            f"Здравствуйте, {request.user.username}!\n\n"
            f"Благодарим за заказ в нашем магазине портативных гаджетов.\n"
            f"Детализированный товарный чек находится во вложении к этому письму.\n\n"
            f"Служба поддержки Portative Shop."
        )

        # Используем EmailMessage для возможности прикрепления файлов
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email],
        )
        
        # Прикрепляем сгенерированный Excel-файл из памяти
        email.attach(
            filename=f"receipt_order_{request.user.id}.xlsx",
            content=excel_buffer.getvalue(),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        email.send()

        # 3. ОЧИСТКА КОРЗИНЫ ПОСЛЕ УСПЕШНОГО ОФОРМЛЕНИЯ
        cart_items.delete()

        messages.success(request, f"Заказ успешно оформлен! Чек отправлен на почту {user_email}.")
        return redirect('product_list')

    return render(request, 'shop/checkout.html', {'cart': cart})
def home_view(request):
    text = (
        "Главная страница магазина портативных гаджетов\n\n"
        "Ссылки на разделы:\n"
        "1. Каталог товаров: /catalog/\n"
        "2. О магазине: /about/\n"
        "3. Об авторе: /author/\n"
    )
    return HttpResponse(text, content_type="text/plain; charset=utf-8")

def about_view(request):
    text = (
        "О магазине\n\n"
        "Данный проект является интернет-магазином портативных гаджетов.\n"
        "Здесь представлен широкий ассортимент мобильной техники, умных часов,\n"
        "аудиосистем, автогаджетов и аксессуаров для умного дома."
    )
    return HttpResponse(text, content_type="text/plain; charset=utf-8")

def author_view(request):
    text = (
        "Об авторе\n\n"
        "Лабораторную работу выполнил:\n"
        "Студент: Иванов Иван Иванович\n"
        "Группа: 123456\n"
        "Проект: Разработка структуры сайта на Django."
    )
    return HttpResponse(text, content_type="text/plain; charset=utf-8")
def product_list(request):
    """Отображение каталога товаров с поиском и фильтрацией."""
    products = Product.objects.all()
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    # Считывание параметров фильтрации из GET-запроса
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    manufacturer_id = request.GET.get('manufacturer', '')

    # Поиск по названию или описанию (Q-объекты)
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Фильтрация по категории
    if category_id:
        products = products.filter(category_id=category_id)

    # Фильтрация по производителю
    if manufacturer_id:
        products = products.filter(manufacturer_id=manufacturer_id)

    context = {
        'products': products,
        'categories': categories,
        'manufacturers': manufacturers,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_manufacturer': manufacturer_id,
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, pk):
    """Детальная информация о конкретном товаре."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})


@login_required
def cart_view(request):
    """Просмотр корзины текущего пользователя."""
    # Получаем или создаем корзину, если её ещё нет
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'shop/cart.html', {'cart': cart})


@login_required
def add_to_cart(request, product_id):
    """Добавление товара в корзину."""
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Ищем, есть ли уже этот товар в корзине
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        # Если товар уже был, увеличиваем количество на 1
        if cart_item.quantity + 1 <= product.stock_quantity:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"Количество товара {product.name} увеличено.")
        else:
            messages.error(request, f"Невозможно добавить больше товара. На складе всего {product.stock_quantity} шт.")
    else:
        # Если товара не было, проверяем доступность хотя бы 1 штуки
        if product.stock_quantity >= 1:
            cart_item.quantity = 1
            cart_item.save()
            messages.success(request, f"Товар {product.name} добавлен в корзину.")
        else:
            messages.error(request, "Товара нет в наличии на складе.")
            cart_item.delete()

    return redirect('product_list')


@login_required
def update_cart(request, item_id):
    """Обновление количества товара напрямую из корзины."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        try:
            new_quantity = int(request.POST.get('quantity', 1))
            if new_quantity <= 0:
                cart_item.delete()
                messages.success(request, "Товар удален из корзины.")
            elif new_quantity <= cart_item.product.stock_quantity:
                cart_item.quantity = new_quantity
                cart_item.save()
                messages.success(request, "Количество товара обновлено.")
            else:
                messages.error(request, f"Ошибка: Доступно только {cart_item.product.stock_quantity} шт.")
        except ValueError:
            messages.error(request, "Введено некорректное число.")
            
    return redirect('cart_view')


@login_required
def remove_from_cart(request, item_id):
    """Удаление позиции из корзины."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Товар удален из корзины.")
    return redirect('cart_view')
