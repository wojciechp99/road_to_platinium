from django.urls import path
from .views import games, GameAchievementsView, AchievementUpdateView

urlpatterns = [
    path('game/<int:pk>', GameAchievementsView.as_view(), name="achiev"),
    path('achiev/update/<int:pk>', AchievementUpdateView.as_view(), name='achiev-update'),
    path('', games, name='index'),
]
