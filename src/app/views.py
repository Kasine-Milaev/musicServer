from django.shortcuts import render, get_object_or_404
from . import models

# Create your views here.

def main(request):
    return render(request, 'app/index.html')

def player(request):
    return render(request, 'app/player.html')

def artists(request):
    artists = models.Artist.objects.all()
    return render(request, 'app/artists.html',{'artists':artists})

def artist(request, slug):
    artist = get_object_or_404(models.Artist, slug=slug)
    albums = models.Album.objects.filter(albumauthor__artist=artist).distinct()
    return render(request, 'app/artist.html', {'artist':artist, 'albums':albums})

def tracks(request):
    return render(request, 'app/tracks.html')

def albums(request):
    albums = models.Album.objects.all()
    return render(request, 'app/albums.html', {'albums':albums})

def album(request, slug):
    album = get_object_or_404(models.Album, slug=slug)
    albumAuthors = models.Artist.objects.filter(albumauthor__album=album)
    albumTracks = album.track_set.all().order_by('order').prefetch_related('trackauthor_set__artist')
    tracks = [None] * album.tracksCount
    for track in albumTracks:
        tracks[track.order-1] = track
    return render(request, 'app/album.html', {'album':album, 'tracks':tracks,'albumAuthors':albumAuthors})
