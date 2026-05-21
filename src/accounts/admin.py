from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AdvancedUser
from .forms import UserCreationForm
from app.models import FavoriteTrack
import logging
# Register your models here.

class FavoriteTrackInline(admin.TabularInline):
    model = FavoriteTrack
    extra = 0
    autocomplete_fields = ['track']

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
    inlines = [FavoriteTrackInline]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


# AdvancedUser._meta.app_label = 'auth'
# AdvancedUser._meta.verbose_name = 'Пользователь'
# AdvancedUser._meta.verbose_name_plural = 'Пользователи'

# admin.site.register(AdvancedUser,CustomUser)