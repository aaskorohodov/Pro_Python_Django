from django.urls import path  # сама функция сопоставления
from .views import *  # из текущего пакета (women) импортируем все функции

urlpatterns = [
    path('', index),
    path('cats/', categories),
]