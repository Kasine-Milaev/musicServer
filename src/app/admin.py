from django.contrib import admin
from .models import Album, Artist, Track, TrackAuthor, AlbumAuthor
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

class TrackAdmin(admin.ModelAdmin):
    inlines = [TrackAuthorInline]

class AlbumAdmin(admin.ModelAdmin):
    inlines = [AlbumAuthorInline,AlbumTracks]

admin.site.register(Album,AlbumAdmin)
admin.site.register(Artist)
admin.site.register(Track,TrackAdmin)