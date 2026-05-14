from django.db import models

# Create your models here.

class Artist(models.Model):
    name = models.CharField(max_length=200)


class Album(models.Model):
    name = models.CharField(max_length=200)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE
    )

class Track(models.Model):
    name = models.CharField(max_length=200)
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE
    )
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE
    )
    path = models.FileField(upload_to='')
