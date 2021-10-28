from django.urls import path, re_path  # сама функция сопоставления (path и re_path - вторая для регулярных выражений)
from .views import *  # из текущего пакета (women) импортируем все функции

urlpatterns = [
    path('', index, name='home'),  # ловим пустой url, вызываем функцию index из отображения.
                                   # name = придуманное имя, по которому можно звать этот путь. Например при редирект
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),  # re_path умеет работать с регулярными выражениями
    path('about/', about, name='about'),
    path('addpage/', addpage, name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    path('category/<int:cat_id>/', show_category, name='category')  # отлавливаем любое число, пакуем в переменную cat_id, передаем в views
]