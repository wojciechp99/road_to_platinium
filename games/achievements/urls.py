from django.urls import path
from .views import games, GameAchievementsView, AchievementUpdateView, change_achievement_status, AchievementDetailView

urlpatterns = [
    path('game/<int:pk>', GameAchievementsView.as_view(), name="achiev"),
    path('achiev/update/<int:pk>', AchievementUpdateView.as_view(), name='achiev-update'),
    path('<int:pk>/change-achievement-status', change_achievement_status, name='change-status'),
    path('achiev/<int:pk>', AchievementDetailView.as_view(), name='achiev-detail'),
    path('', games, name='index'),
]
