# catalog/views.py
from django.http import HttpResponse

def home_view(request):
    text = (
        "Главная страница магазина портативных гаджетов\n\n"
        "Ссылки на разделы:\n"
        "1. О магазине: /about/\n"
        "2. Об авторе: /author/\n"
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
        "Студент: Давидовский Иван Михайлович\n"
        "Группа: 88ТП\n"
        "Проект: Разработка базовой структуры сайта на Django."
    )
    return HttpResponse(text, content_type="text/plain; charset=utf-8")
