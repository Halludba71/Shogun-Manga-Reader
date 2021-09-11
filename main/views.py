from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import manga
# Create your views here.

def redirect_view(response):
    response = redirect('/library')
    return response

def library(response):
    library = manga.objects.all
    return render(response, "main/library.html", {'library': library})

def browse(response):
    return render(response, "main/browse.html")