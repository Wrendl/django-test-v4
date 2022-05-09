from django.contrib import admin
from . import models


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name', )


@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name', )
    list_filter = ('name', )


@admin.register(models.Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'create_at')
    list_display_links = ('title', )
    list_filter = ('genre', 'create_at', )
    # search_fields = ('user', 'genre__name')


@admin.register(models.Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title')
    list_display_links = ('title', )
    list_filter = ('user', )
    search_fields = ('user', 'track__title')


@admin.register(models.SocialLinks)
class SocialLinksAdmin(admin.ModelAdmin):
    list_display = ('id', 'link', 'cover')
    list_display_links = ('link', )


@admin.register(models.Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'avatar', )
    list_display_links = ('name', )

