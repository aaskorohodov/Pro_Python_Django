from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse('Страница приложения women')


def categories(request, catid):  # catid рандомное имя, отлавливается в urls.py
    if request.GET:  # если он есть, то распечатать
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")


def archive(request, year):  # year отлавливается в urls.py
    return HttpResponse(f"<h1>Архив по годам</h1>{year}</p>")