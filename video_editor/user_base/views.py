from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Привет, Глеб! Почему перечень в квадратынх скобках отбивается красной строкой?")