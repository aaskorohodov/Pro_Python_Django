from django.contrib import admin

from.models import *


class WomenAdmin(admin.ModelAdmin):
    '''Класс для удобного отображения данных в админке.
    list_display = что отображать в общем списке
    list_display_links = что из этого сделать кликабельным
    search_fields = появится строка поиска, станет можно искать по указанным тут полям
    list_editable = что можно редактировать прямо из общего списка
    list_filter = добавит справа панель фильтрации, в которой будут указанные тут поля
    prepopulated_fields = автоматическое заполнение поля (слагом), сгенерированным из title
    *буквально одно поле будет заполняться автоматом, когда админ заполняет другое поле
    '''
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)  # обязательно запятая, нужно передавать кортеж
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Women, WomenAdmin)