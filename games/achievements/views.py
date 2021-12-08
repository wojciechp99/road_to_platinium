from django.shortcuts import render
from django.http import HttpResponse
from .models import Game, Achievement


def hello(request):
    return HttpResponse('Hello, world!')


def genres(request):
    return render(request, template_name='games.html',
                  context={'games': Game.objects.all(),
                           'achievements': Achievement.objects.all().count(),
                           'finished': Achievement.objects.all().filter(completed=True).count()
                           })

