from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView

from .models import Game, Achievement
from .forms import AchievementForm


class GameDeleteView(DeleteView):
    template_name = 'game_delete.html'
    model = Game
    success_url = reverse_lazy('index')


class GameCreateView(CreateView):
    template_name = 'forms.html'
    model = Game
    fields = ['name']
    success_url = reverse_lazy('index')


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

    def get_context_data(self, *args, **kwargs):
        context = super(GameAchievementsView, self).get_context_data(*args, **kwargs)
        game = Game.objects.get(slug=self.kwargs['slug'])
        context['filtered'] = Achievement.objects.filter(game=game)
        context['game_name'] = Game.objects.get(slug=self.kwargs['slug'])
        return context


def change_achievement_status(request, pk):
    achievement = Achievement.objects.get(pk=pk)
    if achievement.completed:
        achievement.completed = False
    else:
        achievement.completed = True
    achievement.save()
    game = Game.objects.get(name=achievement.game)
    return HttpResponseRedirect(reverse_lazy('achiev', kwargs={'pk': game.id, 'slug': game.slug}))


def upload_to_database(request, name):
    from django.utils.text import slugify
    import requests

    STEAM_KEY = request.GET.get('steam_key')
    GAME_ID = request.GET.get('game_id')

    get_api = requests.get(
        f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v0002/?key={STEAM_KEY}&appid={GAME_ID}&l=english&format=json")

    if get_api.status_code != 200:
        return render(request, template_name='status_code.html', context={'status_code': get_api.status_code})

    try:
        achievements = (get_api.json()['game']["availableGameStats"]["achievements"])
    except KeyError:
        status = "Game doesn't have achievements on steam, sorry :("
        return render(request, template_name='achievements_missing.html',
                      context={'status': status})

    game = Game.objects.get(name=name)

    from django.core.exceptions import ObjectDoesNotExist
    for index in achievements:
        try:
            if Achievement.objects.get(name=index["displayName"]):
                continue
        except ObjectDoesNotExist:
            if index['hidden'] == 0:
                description = index['description']
            else:
                description = "Description for this achievement is hidden"

            Achievement.objects.create(name=index["displayName"],
                                       game=game,
                                       link=index['icon'],
                                       description=description,
                                       slug=slugify(index["displayName"]))

    return render(request, template_name='games.html', context={'games': Game.objects.all()})


def get_achievements(request, name):
    return render(request, template_name="get_achievements.html", context={'name': name})


def games(request):
    return render(request, template_name='games.html',
                  context={'games': Game.objects.all(),
                           'achievements': Achievement.objects.all().count(),
                           'finished': Achievement.objects.all().filter(completed=True).count()
                           })
