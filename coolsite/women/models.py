from django.db import models
from django.urls import reverse


class Women(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)  # blank=True = может быть пустым
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")  # описывает каталог, куда класть фото (папки)
    time_create = models.DateTimeField(auto_now_add=True)  # auto_now_add не меняется
    time_update = models.DateTimeField(auto_now=True)  # auto_now меняется
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})