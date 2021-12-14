from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import *


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        '''Переписываем значение пустого поля для выпадающего списка (выбор категорий). По умолчанию там черточки,
        пока мы что-то не выберем, хотим, чтобы там был какой-то текст. Для этого переписывает init базового класса.
        Там есть словарь, в нем есть ключ cat, который взят из модели Women, и указывает на категорию (певицы, актрисы).
        У этого ключа есть свойство empty_label, его и переписываем на что захотим.'''
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = Women  # указывает, с какой моделью установить связь
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat'] # какие поля брать (из модели Women)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }
        '''widgets = указывает свой стиль для полей ввода. Title получает TextInput, content получает размер (колонки
        и ряда)'''

    def clean_title(self):
        '''Валидатор, проверяет длину поля. Обязательно начинается с clean_, затем идет имя проверяемого поля.
        Обращаемся к текущей форме (self.), в ней смотрим на cleaned_data по ключу title.'''

        title = self.cleaned_data['title']  # обращаемся к словарю, берем тайтл
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title


# класс ниже более не используется
# class AddPostForm(forms.Form):  # произвольное название, наследуется от forms.Form
#     title = forms.CharField(max_length=255, label='Заголовок')
#     slug = forms.SlugField(max_length=255, label="URL")
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label="Контент")
#     is_published = forms.BooleanField(label="Публикация", required=False, initial=True)
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категории", empty_label="Категория не выбрана")



class RegisterUserForm(UserCreationForm):
    '''Форма для регистрации нового пользователя. Переменные ниже указывают стили для этих полей.'''
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    '''Форма авторизации'''
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()