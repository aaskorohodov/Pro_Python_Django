from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from coolsite import settings
from women.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls'))  # include включает все маршруты из указанного каталога и файла (women.urls)
]

if settings.DEBUG:  # в режиме отладки, когда DEBUG == True
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)