from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.main,name='main'),
    path('player/',views.player,name="player"),

    path('artists/',views.artists, name="artists"),
    path('artists/<slug:slug>/',views.artist, name="artist"),

    path('albums/',views.albums, name="albums"),
    path('albums/<slug:slug>/',views.album, name="album"),

    path('tracks/',views.tracks, name="tracks"),
]