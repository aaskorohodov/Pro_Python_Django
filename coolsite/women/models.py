from django.db import models
from django.urls import reverse


class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(blank=True, verbose_name='Текст статьи')  # blank=True = может быть пустым
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фото')  # описывает каталог, куда класть фото (папки)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')  # auto_now_add не меняется
    time_update = models.DateTimeField(auto_now=True, verbose_name='время изменения')  # auto_now меняется
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    '''cat это ссылка на другую таблицу. on_delete указывает что делать, при удалении записи в другой таблице.
    Category стоит в кавычках, чтобы не было ошибки (потому что класс Category определен ниже). Можно указывать
    без кавычек, но тогда надо поднять класс Category выше класса Women.
    Так как это поле будет ссылаться на другое (ForeignKey), то в таблице гео будут звать cat_id
    null=True даст Django оставить поля пустыми'''
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категории')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        '''Возвращает ссылку на объект этого класса. reverse просит имя маршрута из urls.py, в том маршруте нужна
        какая-то цифра (такой там урл обрабатывается, с цифрой = номер поста), мы ее передаем словарем в kwargs,
        где post_id = имя переменной, которую просит path в urls.py, а self.pk = значение, которое и станет цифрой.
        Если маршрут просит несколько переменных (.../catwgory1/item2.ru), то в словаре можно передать их все.'''
        return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        '''Нужен для красивого-удобного отображения'''
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')  # db_index

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']