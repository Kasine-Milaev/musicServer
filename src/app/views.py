from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
import logging
import json
from django.db.models import OuterRef, Exists
from django.core.exceptions import ValidationError
from django.http import JsonResponse
# Create your views here.
def main(request):
    return render(request, 'app/index.html')

@login_required
def artists(request):
    artists = Artist.objects.all()
    return render(request, 'app/artists.html',{'artists':artists})

@login_required
def artist(request, slug):
    artist = get_object_or_404(Artist, slug=slug)
    albums = artist.albums.all()
    return render(request, 'app/artist.html', {'artist':artist, 'albums':albums})

@login_required
def albums(request):
    albums = Album.objects.all()
    return render(request, 'app/albums.html', {'albums':albums})

@login_required
def album(request, slug):
    user = request.user
    album = get_object_or_404(Album, slug=slug)
    albumAuthors = album.artists.all()
    db_request = Exists(FavoriteTrack.objects.filter(user=user,track=OuterRef('pk')))
    albumTracks = album.tracks.all().order_by('order').prefetch_related('artists').annotate(is_favorite = db_request)
    tracks = [None] * album.tracksCount
    for track in albumTracks:
        for artist in track.artists.all():
            logging.warning(artist.name)
        tracks[track.order-1] = track

    return render(request, 'app/album.html', {'album':album, 'tracks':tracks,'albumAuthors':albumAuthors})

def like_track(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({'error': "Невалидный JSON"},status=400)
        slug = data.get('slug')
        track = get_object_or_404(Track, slug=slug)
        user = request.user
        favorite, created = FavoriteTrack.objects.get_or_create(user = user, track = track)
        if created:
            return JsonResponse({'is_favorite': True},status=200)
        else:
            favorite.delete()
            return JsonResponse({'is_favorite': False},status=200)
    if request.method == 'GET':
        return JsonResponse({'type':'yeah'})


@login_required
def profile(request):
    favorites_tracks = request.user.tracks.all().prefetch_related('artists','album__artists')
    return render(request, 'app/profile.html', {'favorites':favorites_tracks})
