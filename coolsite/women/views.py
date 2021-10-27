from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render
from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


def index(request):
    # posts = Women.objects.all()  # берем все записи модели, ниже передаем их в шаблон
    # cats = Category.objects.all()  # и эти записи тоже берем. В шаблон передаем словарем ниже. Более не требуется

    '''Это словарь, чтобы передавать параметры в шаблоны. Можно прописать параметры ниже в рендер, но так красивше.
    Ниже нужно передать этот словарь context в специальную переменную context (словарь можно назвать иначе,
    а переменная именно context'''
    context = {
        # 'posts': posts,
        # 'cats': cats, более не требуется, работает на пользовательском теге
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': 0,
    }  # cat_selected, чтобы на главной отображалась одна из записей как строка, а не как ссылка. В шаблоне есть if,
       # он реагирует на cat_selected
    return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})


def categories(request, catid):  # catid рандомное имя, отлавливается в urls.py
    if request.GET:  # если он есть, то распечатать
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")


def archive(request, year):  # year отлавливается в urls.py
    return HttpResponse(f"<h1>Архив по годам</h1>{year}</p>")


def addpage(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")


def pageNotFound(request, exeption):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def show_category(request, cat_id):
    posts = Women.objects.filter(cat_id=cat_id)  # нужно только чтобы поднять 404

    if len(posts) == 0:
        raise Http404()

    context = {
        'menu': menu,
        'title': 'Рубрики',
        'cat_selected': cat_id,
    }

    return render(request, 'women/index.html', context=context)