from django.urls import path
from .views import games, GameAchievementsView, AchievementUpdateView, change_achievement_status, AchievementDetailView, \
    upload_to_database, get_achievements, GameCreateView, GameDeleteView

urlpatterns = [
    path('game/<int:pk>/<str:slug>', GameAchievementsView.as_view(), name="achiev"),
    path('achiev/update/<int:pk>', AchievementUpdateView.as_view(), name='achiev-update'),
    path('change-achievement-status/<int:pk>', change_achievement_status, name='change-status'),
    path('achiev/<int:pk>', AchievementDetailView.as_view(), name='achiev-detail'),
    path("upload-achievements/<str:name>", upload_to_database, name='upload-achievements'),
    path('get-achievements-from-steam/<str:name>', get_achievements, name='get_achievements'),
    path('create-game', GameCreateView.as_view(), name='create-game'),
    path('delete-game/<int:pk>', GameDeleteView.as_view(), name='delete-game'),
    path('', games, name='index'),
]
