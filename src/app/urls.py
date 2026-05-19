from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.main,name='main'),

    path('artists/',views.artists, name="artists"),
    path('artists/<slug:slug>/',views.artist, name="artist"),

    path('albums/',views.albums, name="albums"),
    path('albums/<slug:slug>/',views.album, name="album"),


    path('plofile/',views.profile, name="profile")
]