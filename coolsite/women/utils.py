from django.db.models import Count

from .models import *


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


class DataMixin:
    def get_user_context(self, **kwargs):

        context = kwargs  # формируем начальный словарь из тех kwargs, которые были переданные строчкой выше
        # это нужно, чтобы можно было докидать в него еще чего-нибудь
        # ожидаем принять, например, title, который передаст views.py. Title будет разный, в зависимости от класса там

        '''Строчка ниже не только читает все записи, но и дополняет коллекцию так, что становится можно посчитать
        сколько там чего. Это нужно в шаблоне, чтобы не показывать пустые категории. Для всего остального, это обычная
        коллекция, в которой будут все данные модели (все записи по модели из БД)'''
        cats = Category.objects.annotate(Count('women'))

        '''Далее делается проверка, авторизован ли пользователь. Если нет, то из меню убирается пункт Добавить статью.
        Для этого копируем меню в экземпляр, проверяем пользователя на авторизацию (self.request.user.is_authenticated
        это свойство, его можно посмотреть). Если он не авторизован, то делаем pop второй элемент (это нужная кнопка).'''
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
                user_menu.pop(1)

        context['menu'] = user_menu  # докидываем меню
        context['cats'] = cats  # и пакуем категории

        '''Дале проверяем, передали мы в эту функцию ключ cat_selected. Если не передали, знакчит запишем его = 0.
        Он нужен, чтобы в правом меню подсветить выбранную категорию. 0 = выбрано "все категории". Если cat_selected
        сюда передается, то из шаблона'''
        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        return context
