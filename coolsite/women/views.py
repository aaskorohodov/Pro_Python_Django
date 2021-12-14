from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from .forms import *
from .models import *
from .utils import *


class WomenHome(DataMixin, ListView):
    model = Women  # указываем модель
    template_name = 'women/index.html'  # указываем, какой шаблон брать. Иначе может взять не то
    context_object_name = 'posts'  # указываем имя коллекции, которую Джанго автоматически сделает и передаст в шаблон
    '''Эта коллекция делается автоматически из модели, по умолчанию ее имя object_list. В ней все записи модели'''

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Передает в шаблон дополнительные данные. Предварительно берет уже имеющиеся данные, которые были добыты
        автоматически, и распаковывает их в словарь (context = super().get_context_data(**kwargs)) (например,
        автоматически были добыты все записи из базы, выше мы переименовали их в posts). Затем к этому
        словарю добавляются любые другие данные.'''
        context = super().get_context_data(**kwargs)

        # ниже закомментировано, заменено на еще ниже (на миксин)
        # context['title'] = 'Главная страница'
        # context['cat_selected'] = 0  # чтобы подсветить справа кнопку "все категории", ведь мы тут, пускай светится
        # context['menu'] = menu  # Главное меню в шапке
        # return context

        '''Этот класс (WomenHome) наследуется от нескольких классов, втч от миксина DataMixin. В нем есть метод 
        get_user_context, который можно позвать на экземпляр. Он вернет нужный подготовленный контекст. Но у нас уже
        есть часть контекста (данные из БД), так что можно либо слить два словаря в один и в переменную, а затем
        эту переменную передать в шаблон, либо просто сделать return слитого воедино словаря, без переменной.
        Шаблону все равно, в каком виде ему передают контекст, он так и так его развернет и достанет оттуда все.
        Ниже словари сливаются в 1 переменную – сначала в 1 список, затем в словарь.'''

        c_def = self.get_user_context(title="Главная страница")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        '''Добывает из модели только те данные, которые отмечены как опубликованные. Чтобы отображать только их, а те,
        у которых стоит метка "не опубликовано", не выводить. get_queryset = специальное имя функции, для такой задачи
        именно его и надо определять.

        *сам по себе get_queryset определяет любое правило, которым мы хотим читать модель. Как шаблонный фильтр.'''

        '''.select_related('cat') делает жадную загрузку. Без него, при отрисовке записей (посты в списке постов),
        на каждую запись делается свой запрос. Запрос делает шаблон, чтобы показать категорию (актрисы/певицы).
        Следовательно, сколько записей на странице, столько и запросов к БД.
        select_related делает 1 запрос на все нужное, оптимизация. Запрос становится жадным, он делается не столько
        раз, сколько раз его делает шаблон в своем цикле for, а 1 раз.'''

        return Women.objects.filter(is_published=True).select_related('cat')


# def index_not_used_any_more(request):
#     # posts = Women.objects.all()  # берем все записи модели, ниже передаем их в шаблон  более не требуется
#     # cats = Category.objects.all()  # и эти записи тоже берем. В шаблон передаем словарем ниже. Более не требуется
#
#     '''Это словарь, чтобы передавать параметры в шаблоны. Можно прописать параметры ниже в рендер, но так красивше.
#     Ниже нужно передать этот словарь context в специальную переменную context (словарь можно назвать иначе,
#     а переменная именно context)'''
#     context = {
#         # 'posts': posts, более не требуется
#         # 'cats': cats, более не требуется, работает на пользовательском теге
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }  # cat_selected, чтобы на главной отображалась одна из записей как строка, а не как ссылка. В шаблоне есть if,
#        # он реагирует на cat_selected  более не требуется
#     return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})


def categories(request, catid):  # catid рандомное имя, отлавливается в urls.py
    if request.GET:  # если он есть, то распечатать. request.GET это коллекция http запросов (?name=asd&title=...)
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")


def archive(request, year):  # year отлавливается в urls.py
    return HttpResponse(f"<h1>Архив по годам</h1>{year}</p>")


class AddPage(DataMixin, CreateView):
    '''Так как в модели указан get_absolut_url, то после добавления записи, Django воспользуется им, чтобы перенаправится
    на свеже-созданную страницу.'''

    form_class = AddPostForm  # указываем форму из forms.py
    template_name = 'women/addpage.html'
    # success_url = reverse_lazy('home')
    '''success_url указывает, куда направиться в случае успешной записи. reverse_lazy вместо reverse, потому что модель
    еще не создана, что-то такое. reverse_lazy безопаснее в общем.'''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # context['title'] = 'Добавление статьи'
        # context['menu'] = menu

        c_def = self.get_user_context(title="Добавление статьи")
        context = dict(list(context.items()) + list(c_def.items()))
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


# def contact(request):
#     return HttpResponse("Обратная связь")


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# def login(request):
#     return HttpResponse("Авторизация")


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'  # по умолчанию ищет в urls.py переменную slug, переопределяем ее на другое имя
    context_object_name = 'post'  # как именовать переменную, передаваемую в контекст (по умолчанию другое имя)

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Передаем дополнительные данные в шаблон'''

        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])  # смотрим на этот ключ из добытых данных. ХЗ почему он такой

        return dict(list(context.items()) + list(c_def.items()))


        # context['title'] = context['post']
        # context['menu'] = menu
        # return context


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


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False  # 404, если модель пуста (введен неверный урл, в нашем случае)
    '''allow_empty нужен, так как ниже, когда мы передаем в шаблон доп контекст, мы обращаемся к словарю по индексу.
    А словарь автоматически добыт из модели. Если мы ввели некорректный урл, то модель вернет пустой словарь,
    обращение по индексу вызовет ошибку. С allow_empty не вызовет.'''

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
        '''Ниже обращаемся к коллекции данных из модели, берем первую запись, оттуда берем cat = название категории,
        превращаем его в строку и склеиваем с "Категория". Получаем "категория такая-то".
        Ниже похожим образом берем номер категории, чтобы подсветить в правом меню выбранный раздел.'''

        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        # context['menu'] = menu
        # context['cat_selected'] = context['posts'][0].cat_id
        # return context

        '''Ниже делаем тайтл, путем обращения по первой модели Women (не важно какая там), к связанной таблице (.cat).
        Оттуда вернется название рубрики, клеим его к слову Категория. Еще передаем номер категории, чтобы подсветить
        в меню слева выбранную категорию.
        В первом случае берем cat = название, во втором случае берем сat_id = номер категории.'''

        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)

        return dict(list(context.items()) + list(c_def.items()))


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


class RegisterUser(DataMixin, CreateView):
    '''Регистрация нового пользователя'''
    form_class = RegisterUserForm  # связанный класс формы
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        '''Вызывается, в случае успешной регистрации. Делает автоматическую авторизацию свежим пользователем.'''
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    '''Авторизация пользователя'''
    form_class = LoginUserForm  # связанный класс формы
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        '''Куда отправиться, в случае успеха'''
        return reverse_lazy('home')


def logout_user(request):
    '''Функция, которую вызывает кнопка Выйти. Делает logout и редирект.'''
    logout(request)
    return redirect('login')