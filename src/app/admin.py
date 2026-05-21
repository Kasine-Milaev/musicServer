from django.contrib import admin
from .models import *
# Register your models here.

class TrackAuthorInline(admin.TabularInline):
    model = TrackAuthor
    extra = 0

class AlbumAuthorInline(admin.TabularInline):
    model = AlbumAuthor
    extra = 0

class AlbumTracks(admin.TabularInline):
    model = Track
    extra = 0 
    ordering = ['order']

class FavoritesTrackInline(admin.TabularInline):
    model = FavoriteTrack
    extra = 0

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    search_fields = ['name','slug']
    list_display = ['name','album']

    inlines = [TrackAuthorInline,FavoritesTrackInline]

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['name','slug']
    list_display = ['name','get_artist_name']
    inlines = [AlbumAuthorInline,AlbumTracks]

    @admin.display(description="Артист")
    def get_artist_name(self,obj):
        authors = obj.artists.all()
        artist_names = []
        for author in authors:
            if author.name:
                artist_names.append(author.name)
        return ", ".join(artist_names)

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    search_fields = ['name','slug']
    inlines = [AlbumAuthorInline]

    