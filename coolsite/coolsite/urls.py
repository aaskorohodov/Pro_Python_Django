from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from coolsite import settings
from women.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls'))  # include включает все маршруты из указанного каталога и файла (women.urls)
    # то есть все после домена (''), будет браться из urls.py конкретного приложения
]

if settings.DEBUG:  # в режиме отладки, когда DEBUG == True, добавляем еще 1 маршрут для статических файлов (картинок)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    '''
    settings.MEDIA_URL = переменная MEDIA_URL из settings.py, в ней указан /media/ и все
    document_root также указывает на файл settings, там переменная, которая готовит путь до файла на сервере
    '''