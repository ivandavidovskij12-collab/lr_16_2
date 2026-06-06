# catalog/urls.py
from django.urls import path
from .views import home_view, about_view, author_view

urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('author/', author_view, name='author'),
]
