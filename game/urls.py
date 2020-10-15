from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('unfinished/', views.unfinished_games, name='unfinished_games'),
    path('finished/', views.finished_games, name='finished_games'),        
    path('new/', views.new_game, name='new_game'),
    path('<int:game_pk>/play/', views.play_game, name='play_game'),
    path('<int:game_pk>/view', views.view_game, name='view_game'),
    path('<int:game_pk>/finish', views.finish_game, name='finish_game'),
    path('<int:game_pk>/delete', views.delete_game, name='delete_game'),
]