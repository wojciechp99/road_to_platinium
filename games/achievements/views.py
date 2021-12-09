from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView

from .models import Game, Achievement
from .forms import AchievementForm


class AchievementDetailView(DetailView):
    template_name = 'achievement_detail.html'
    model = Achievement
    context_object_name = 'achievement'


class AchievementUpdateView(UpdateView):
    template_name = 'forms.html'
    model = Achievement
    form_class = AchievementForm
    # fields = '__all__'
    success_url = reverse_lazy('index')


class GameAchievementsView(ListView):
    template_name = 'games_all_achiev.html'
    model = Achievement
    context_object_name = 'achievements'


def change_achievement_status(request, pk):
    achievement = Achievement.objects.get(pk=pk)
    if achievement.completed:
        achievement.completed = False
    else:
        achievement.completed = True
    achievement.save()
    game = Game.objects.get(name=achievement.game)
    return HttpResponseRedirect(reverse_lazy('achiev', kwargs={'pk': game.id}))


def games(request):
    return render(request, template_name='games.html',
                  context={'games': Game.objects.all(),
                           'achievements': Achievement.objects.all().count(),
                           'finished': Achievement.objects.all().filter(completed=True).count()
                           })

