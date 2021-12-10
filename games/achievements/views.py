from django.http import HttpResponseRedirect, HttpRequest
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


def upload_to_database(request):
    from django.utils.text import slugify
    import requests

    STEAM_KEY = "0"  # for now key is stored as value
    GAME_ID = "211420"  # page for obtaining game id: https://steamdb.info/ , for now also stored as value

    get_api = requests.get(
        f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v0002/?key={STEAM_KEY}&appid={GAME_ID}&l=english&format=json")
    achievements = (get_api.json()['game']["availableGameStats"]["achievements"])
    game = Game.objects.get(name="Dark Souls")

    for index in achievements:
        if Achievement.objects.get(name=index["displayName"]):
            continue

        if index['hidden'] == 0:
            description = index['description']
        else:
            description = "Description for this achievement is hidden"

        Achievement.objects.create(name=index["displayName"],
                                   game=game,
                                   link=index['icon'],
                                   description=description,
                                   slug=slugify(index["displayName"]))

    return render(request, template_name='games_all_achiev.html', context={'achievements': Achievement.objects.all()})


def games(request):
    return render(request, template_name='games.html',
                  context={'games': Game.objects.all(),
                           'achievements': Achievement.objects.all().count(),
                           'finished': Achievement.objects.all().filter(completed=True).count()
                           })
