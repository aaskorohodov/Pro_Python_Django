from django import template  # модуль работы с шаблонами
from women.models import *  # все модели, для чтения из БД

register = template.Library()  # регистрируется тег, обязательно в переменной register


@register.simple_tag(name='getcats')  # декоратор превращает функцию в тег, опционально можно задать name
def get_categories():  # имя функции произвольное
    '''Возвращает все категории'''
    return Category.objects.all()


@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_selected=0):  # любое имя + (передаем параметры из шаблона, куда этот тег встанет)
    if not sort:
        cats = Category.objects.all() # читаем все категории, данные пакуем в cats
    else:
        cats = Category.objects.order_by(sort)  # или читаем и сортируем как-либо

    return {"cats": cats, "cat_selected": cat_selected} # словарь автоматически передастся в шаблон, указанный выше


@register.inclusion_tag('women/all_posts.html')
def show_all_posts(cat_selected):
    '''Рисует все посты для разных категорий или для главной страницы'''

    if cat_selected != 0:  # сценарий для категорий (что-либо выбрано
        posts = Women.objects.filter(cat_id=cat_selected)
        # test = Women.objects.get(id=5).time_create
        # print(test)

        '''cat_id = название в базе, cat_selected = переменная'''

    else:  # сценарий главной страницы (ничего не выбрано)
        posts = Women.objects.all()

    return {'posts': posts}