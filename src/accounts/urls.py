from django.urls import path, include
from . import views

urlpatterns = [
    path('login/',views.login,name="login"),
    path('registration/',views.registration, name="registration"),
    path('logout/',views.logout, name="logout"),
    path('password-change', views.change_password.as_view(), name='change_password')
]