from django.shortcuts import render
from .utils import comprobar_hay_un_csv

# Create your views here.

def index(request):
    context = {}
    context['hay_csv'] = comprobar_hay_un_csv()
    return render(request, 'index.html', context)