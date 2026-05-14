from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.main,name='main'),
    path('player/',views.player,name="player"),
]