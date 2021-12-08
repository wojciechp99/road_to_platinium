from django.urls import path
from .views import games

urlpatterns = [
    path('', games, name='index')
]
