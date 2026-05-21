from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.conf import settings
# Create your models here.

class Artist(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    cover = models.ImageField(upload_to='artists/',null=True,blank=True) 

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Album(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    cover = models.ImageField(upload_to='albums/',null=True,blank=True)
    tracksCount = models.PositiveSmallIntegerField(default=0)

    artists = models.ManyToManyField(
        Artist,
        through="AlbumAuthor", 
        related_name="albums"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Track(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    album = models.ForeignKey(
        Album,
        related_name='tracks',
        on_delete=models.CASCADE
    )
    path = models.FileField(upload_to='tracks/')
    order = models.PositiveSmallIntegerField(default=0)

    artists = models.ManyToManyField(
        Artist,
        through="TrackAuthor",
        related_name="tracks"
    )

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='FavoriteTrack',
        related_name='tracks'
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class TrackAuthor(models.Model):
    track = models.ForeignKey(Track,
                              on_delete=models.CASCADE
                              )
    artist = models.ForeignKey(Artist,
                               on_delete=models.CASCADE)
    class Meta:
        unique_together = ('track','artist')

class FavoriteTrack(models.Model):
    track = models.ForeignKey(Track, 
                             # В даминке будет писать Трек, _ - для перевода
                             verbose_name=_("Трек"),
                             on_delete=models.CASCADE
                             )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             # В даминке будет писать Пользователь, _ - для перевода
                             verbose_name=_("Пользователь"), 
                             on_delete=models.CASCADE
                             )
    class Meta:
        verbose_name = _("Любимый трек")
        verbose_name_plural = _("Любимые треки")
        unique_together = ('track','user')

class AlbumAuthor(models.Model):
    album = models.ForeignKey(
        Album,  
        on_delete=models.CASCADE
    )
    artist = models.ForeignKey(
        Artist, 
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('album','artist')