from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


class WomenHome(ListView):
    model = Women  # указываем модель
    template_name = 'women/index.html'  # указываем, какой шаблон брать
    context_object_name = 'posts'  # указываем имя коллекции, которую Джанго автоматически сделает и передаст в шаблон
    '''Эта коллекция делается автоматически из модели, по умолчанию ее имя object_list'''

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Передает в шаблон дополнительные данные. Предварительно берет уже имеющиеся данные, которые были добыты
        автоматически, и распаковывает их в словарь (context = super().get_context_data(**kwargs)). Затем к этому
        словарю добавляются любые другие данные.'''
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        context['menu'] = menu
        return context

    def get_queryset(self):
        '''Добывает из модели только те данные, которые отмечены как опубликованные'''
        return Women.objects.filter(is_published=True)


def index_not_used_any_more(request):
    # posts = Women.objects.all()  # берем все записи модели, ниже передаем их в шаблон  более не требуется
    # cats = Category.objects.all()  # и эти записи тоже берем. В шаблон передаем словарем ниже. Более не требуется

    '''Это словарь, чтобы передавать параметры в шаблоны. Можно прописать параметры ниже в рендер, но так красивше.
    Ниже нужно передать этот словарь context в специальную переменную context (словарь можно назвать иначе,
    а переменная именно context'''
    context = {
        # 'posts': posts, более не требуется
        # 'cats': cats, более не требуется, работает на пользовательском теге
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': 0,
    }  # cat_selected, чтобы на главной отображалась одна из записей как строка, а не как ссылка. В шаблоне есть if,
       # он реагирует на cat_selected  более не требуется
    return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})


def categories(request, catid):  # catid рандомное имя, отлавливается в urls.py
    if request.GET:  # если он есть, то распечатать. request.GET это коллекция http запросов (?name=asd&title=...)
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")


def archive(request, year):  # year отлавливается в urls.py
    return HttpResponse(f"<h1>Архив по годам</h1>{year}</p>")


class AddPage(CreateView):
    form_class = AddPostForm  # указываем форму из forms.py
    template_name = 'women/addpage.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        context['menu'] = menu
        return context


# def addpage(request):
#     if request.method == 'POST':  # если request стал POST (форма была отправлена)
#         form = AddPostForm(request.POST, request.FILES)  # формируем форму на основе словаря POST, где лежат заполненные данные
#         # и передает файл (request.FILE), это для отправки фото
#
#         if form.is_valid():  # если все норм, то написать очищенные данные в консоли
#             form.save()  # сохранение для формы, связанной с моделью
#             return redirect('home')
#
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'  # по умолчанию ищет в urls.py переменную slug, переопределяем ее на другое имя
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Передаем дополнительные данные в шаблон'''
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)  # get_object_or_404 функция Джанго, либо найдет объект, либо 404
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'women/post.html', context=context)


def pageNotFound(request, exeption):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class WomenCategory(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False  # 404, если модель пуста (введен неверный урл)

    def get_queryset(self):
        '''Добывает из модели не все данные, а только определенные. Вот какие:
        Обращаемся к таблице Women и фильтруем ее Women.objects.filter
        cat__slug = обращаемся к полю cat, которое ссылается на другую таблицу, в которой берем slug (актрисы или певицы)
        cat__slug должен быть равен текущей категории, которую надо получить из урла. Вот как:
        из текущего запроса берем все данные (данные которые передает urls.py), из них берем cat_slug. Все это выглядит:
        .kwargs['cat_slug']'''

        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        '''Ниже обращаемся к коллекции данных из модели, берем первую запись, оттуда берем cat = название категории'''
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['menu'] = menu
        context['cat_selected'] = context['posts'][0].cat_id
        return context


# def show_category(request, cat_id):
#     posts = Women.objects.filter(cat_id=cat_id)  # нужно только чтобы поднять 404
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'menu': menu,
#         'title': 'Рубрики',
#         'cat_selected': cat_id,
#     }
#
#     return render(request, 'women/index.html', context=context)