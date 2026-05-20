from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as form_login, logout as form_logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import MyUserCreationForm, UserProfileForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
import json
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
    for error in form.errors.values():
        logging.warning(error)
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

class change_password(LoginRequiredMixin,PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('profile')
    def form_valid(self,form):
        messages.success(self.request, "Ваш пароль был успешно изменен!")
        return super().form_valid(form)

def validate(request):
    logging.warning("Validate вызван")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({'error': "Невалидный JSON"},status=400)
        if not data:
            return JsonResponse({'error': "Данные не предоставлены"},status=400)
        ALLOWED_FIELDS = ['username', 'email','password']
        type = data.get('field')
        value = data.get('value','')
        if not type:
            return JsonResponse({'error':"Значение не передано"},status =400)
        form = MyUserCreationForm(data= {type: value})
        is_form_valid = form.is_valid()

        if type in form.errors:
            return JsonResponse({
                'valid':False,
                'message': form.errors[type][0]
                })

        clean_method_name = f'clean_{type}'

        if hasattr(form,clean_method_name):
            try:
                getattr(form,clean_method_name)()
            except ValidationError as e:
                return JsonResponse({
                    'valid':False,
                    'message': e.message
                })
        else:
            return JsonResponse({'error':f'Валидатор не найден'},status=400)
        return JsonResponse({'valid':True})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш профиль успешно изменен")
            return redirect("profile")
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html')
@login_required
def logout(request):
    form_logout(request)
    return redirect('/')