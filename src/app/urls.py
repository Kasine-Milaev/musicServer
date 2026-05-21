from django.urls import path, include
from . import views
from accounts import views as accounts_views

urlpatterns = [
    path('',views.main,name='main'),

    path('artists',views.artists, name="artists"),
    path('artists/<slug:slug>',views.artist, name="artist"),

    path('albums',views.albums, name="albums"),
    path('albums/<slug:slug>',views.album, name="album"),


    path('profile',views.profile, name="profile"),

    path('profile/edit',accounts_views.edit_profile, name = "edit_profile"),

    path('like-track', views.like_track, name="like_track")
]