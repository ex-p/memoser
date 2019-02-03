import os

from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse(os.environ.get('DATABASE_URL'))
