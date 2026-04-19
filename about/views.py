from django.shortcuts import render

from core.theme import template_path


def index(request):
    return render(request, template_path('about.html'))
