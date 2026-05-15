from django.db import models
from django.utils.text import slugify
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
        on_delete=models.CASCADE
    )
    path = models.FileField(upload_to='tracks/')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class TrackAuthor(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('track','artist')

class AlbumAuthor(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('album','artist')