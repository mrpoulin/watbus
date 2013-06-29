from django.shortcuts import render
from django.http import HttpResponse

def favourites(request):
    return render(request, 'easygrt/index.html')

def map(request):
    return render(request, 'easygrt/map.html')

def browse(request):
    return render(request, 'easygrt/browse.html')
