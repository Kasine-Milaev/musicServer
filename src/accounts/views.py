from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as form_login, logout as form_logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import MyUserCreationForm
import logging
# Create your views here.

def login(request):
    if request.method == 'POST':
        # Передаем данные из формы в стандартный класс Django
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            form_login(request, user)
            return redirect('/') 
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})

def registration(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            form_login(request, user)
            return redirect('/')
    else:
        form = MyUserCreationForm()
    for error in form.errors.values():
        logging.warning(error)
    return render(request, 'accounts/register.html', {'form': form})

class change_password(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('profile')
    def form_valid(self,form):
        messages.success(self.request, "Ваш пароль был успешно изменен!")
        return super().form_valid(form)

def logout(request):
    form_logout(request)
    return redirect('/')