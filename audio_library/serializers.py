from rest_framework import serializers

from base.services import delete_old_file
from . import models


class BaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)


class GenreSerializer(BaseSerializer):
    class Meta:
        model = models.Genre
        fields = ('id', 'name', )


class SocialLinksSerializer(BaseSerializer):
    class Meta:
        model = models.SocialLinks
        fields = ('id', 'link', )


class CreateArtistSerializer(BaseSerializer):
    class Meta:
        model = models.Artist
        fields = ('id', 'name', 'avatar', 'social_links', )

    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class ArtistSerializer(CreateArtistSerializer):
    social_links = SocialLinksSerializer(many=True, read_only=True)


class CreateAlbumSerializer(BaseSerializer):
    class Meta:
        model = models.Album
        fields = ('id', 'author', 'name', 'description', 'cover', 'private', )

    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class AlbumSerializer(CreateAlbumSerializer):
    author = ArtistSerializer(many=True, read_only=True)


class CreateAuthorTrackSerializer(BaseSerializer):
    plays_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Track
        fields = (
            'id',
            'title',
            'genre',
            'album',
            'file',
            'create_at',
            'plays_count',
            'playlists'
        )

    def update(self, instance, validated_data):
        delete_old_file(instance.file.path)
        return super().update(instance, validated_data)


class AuthorTrackSerializer(CreateAuthorTrackSerializer):
    genre = GenreSerializer(many=True)
    album = AlbumSerializer()


class CreatePlayListSerializer(BaseSerializer):
    class Meta:
        model = models.Playlist
        fields = ('id', 'title', 'tracks', 'cover', )

    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class PlayListSerializer(CreatePlayListSerializer):
    tracks = AuthorTrackSerializer(many=True, read_only=True)
