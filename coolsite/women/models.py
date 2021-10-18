from django.db import models

class Women(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)  # blank=True = может быть пустым
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")  # описывает каталог, куда класть фото (папки)
    time_create = models.DateTimeField(auto_now_add=True)  # auto_now_add не меняется
    time_update = models.DateTimeField(auto_now=True)  # auto_now меняется
    is_published = models.BooleanField(default=True)