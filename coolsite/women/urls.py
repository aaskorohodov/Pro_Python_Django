from django.urls import path, re_path  # сама функция сопоставления (path и re_path - вторая для регулярных выражений)
from .views import *  # из текущего пакета (women) импортируем все функции

urlpatterns = [
    path('', WomenHome.as_view(), name='home'),  # ловим пустой url, класс WomenHome из views. Для класса as_view()
                                   # name = придуманное имя, по которому можно звать этот путь. Например при редирект
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),  # re_path умеет работать с регулярными выражениями
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category')
]