from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as form_login
# Create your views here.

def login(request):
    if request.method == 'POST':
        # Передаем данные из формы в стандартный класс Django
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            form_login(request, user)
            return redirect('/') 
    return render(request, 'accounts/login.html')

def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            form_login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})