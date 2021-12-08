from django.urls import path
from .views import genres

urlpatterns = [
    path('', genres, name='index')
]
