from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('welcome to sunshoppers')


# Create your views here.
def homepage(request):
    return render(request, 'home.html')
