from rest_framework import serializers

from base.services import delete_old_file
from . import models


class BaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)


class GenreSerializer(BaseSerializer):
    class Meta:
        model = models.Genre
        fields = ('id', 'name', )


class AlbumSerializer(BaseSerializer):
    class Meta:
        model = models.Album
        fields = ('id', 'user_name', 'name', 'description', 'cover', 'private', )

    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


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
