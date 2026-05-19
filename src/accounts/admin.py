from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AdvancedUser
from .forms import UserCreationForm
import logging
# Register your models here.
@admin.register(AdvancedUser)
class CustomUser(UserAdmin):
    add_form = UserCreationForm
    model = AdvancedUser
    list_display = ['username','email','is_staff', 'is_active']
    
    fieldsets = tuple(UserAdmin.fieldsets) + (
        ('Дополнительно', {'fields':('cover',)}),
        )
    
    logging.warning(fieldsets)
    add_fieldsets = UserAdmin.add_fieldsets

# AdvancedUser._meta.app_label = 'auth'
# AdvancedUser._meta.verbose_name = 'Пользователь'
# AdvancedUser._meta.verbose_name_plural = 'Пользователи'

# admin.site.register(AdvancedUser,CustomUser)