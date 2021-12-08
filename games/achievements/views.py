from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from .models import Game, Achievement


class AchievementUpdateView(UpdateView):
    template_name = 'forms.html'
    model = Achievement
    fields = '__all__'
    success_url = reverse_lazy('index')


class GameAchievementsView(ListView):
    template_name = 'games_all_achiev.html'
    model = Achievement
    context_object_name = 'achievements'


def games(request):
    return render(request, template_name='games.html',
                  context={'games': Game.objects.all(),
                           'achievements': Achievement.objects.all().count(),
                           'finished': Achievement.objects.all().filter(completed=True).count()
                           })

