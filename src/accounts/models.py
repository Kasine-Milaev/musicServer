from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
class AdvancedUser(AbstractUser):
    cover = models.ImageField(upload_to='avatars/',verbose_name='Аватарка', blank=True, null=True)