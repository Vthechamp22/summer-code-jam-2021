from django.urls import path
from . import views

urlpatterns = [
    path('', views.music_player, name='music-home'),
    #path('delete_music/', views.delete_music, name='music-delete')
    path('add_music/', views.add_music, name='add-music')
]
