import os
from itertools import chain

from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import render
from rest_framework import generics, parsers, viewsets, views, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from base.classes import MixedSerializer
from base.services import delete_old_file, get_liked_cover
from . import models, serializers


class GenreView(generics.ListAPIView):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class SocialLinksView(generics.ListAPIView):
    queryset = models.SocialLinks.objects.all()
    serializer_class = serializers.SocialLinksSerializer


class ArtistView(MixedSerializer, viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializers.CreateArtistSerializer
    serializer_classes_by_action = {
        'list': serializers.ArtistSerializer
    }

    def get_queryset(self):
        return models.Artist.objects.filter()
        # return models.Album.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        delete_old_file(instance.avatar.path)
        instance.delete()


class OneArtistView(MixedSerializer, viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    serializer_classes_by_action = {
        'list': serializers.AuthorTrackSerializer,
        # 'list': serializers.AlbumSerializer
    }

    def get_queryset(self):
        album = models.Album.objects.filter(author=self.kwargs.get('pk'))
        return models.Track.objects.filter(album=album[0].id)


class AlbumView(MixedSerializer, viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializers.CreateAlbumSerializer
    serializer_classes_by_action = {
        'list': serializers.AlbumSerializer
    }

    def get_queryset(self):
        return models.Album.objects.filter()

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class OneAlbumView(MixedSerializer, viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    serializer_classes_by_action = {
        'list': serializers.AuthorTrackSerializer
    }

    def get_queryset(self):
        # album = models.Album.objects.filter(id=1)
        return models.Track.objects.filter(album=self.kwargs.get('pk'))


class PublicAlbumView(generics.ListAPIView):
    serializer_class = serializers.AlbumSerializer

    def get_queryset(self):
        return models.Album.objects.filter(user__id=self.kwargs.get('pk'), private=False)


class TrackView(MixedSerializer, viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    # permission_classes = [IsAuthor]
    serializer_class = serializers.CreateAuthorTrackSerializer
    serializer_classes_by_action = {
        'list': serializers.AuthorTrackSerializer
    }

    def get_queryset(self):
        return models.Track.objects.filter()

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        delete_old_file(instance.file.path)
        instance.delete()


class PlayListView(MixedSerializer, viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    # permission_classes = [IsAuthor]
    serializer_class = serializers.CreatePlayListSerializer
    serializer_classes_by_action = {
        'list': serializers.PlayListSerializer
    }

    def get_queryset(self):
        all_playlist = models.Playlist.objects.filter(user=self.request.user)
        return all_playlist.exclude(title='Liked songs')

    def perform_create(self, serializer):
        if not models.Playlist.objects.filter(user=self.request.user, title='Liked songs').exists():
            liked_model = models.Playlist(user=self.request.user, title='Liked songs',
                                          cover=get_liked_cover())
            liked_model.save()
        elif self.request.POST['title'] != 'Liked songs':
            serializer.save(user=self.request.user)
        else:
            return Response({"detail": "already have liked songs"}, status=status.HTTP_200_OK)

    def destroy(self, request,  *args, **kwargs):
        instance = self.get_object()
        delete_old_file(instance.cover.path)
        self.perform_destroy(instance)
        return Response({"detail": "deleted"}, status=status.HTTP_200_OK)


class OnePlayListView(MixedSerializer, viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    # permission_classes = [IsAuthor]
    serializer_class = serializers.CreatePlayListSerializer
    serializer_classes_by_action = {
        'list': serializers.PlayListSerializer
    }

    def get_queryset(self):
        return models.Playlist.objects.filter(user=self.request.user, id=self.kwargs.get('pk'))

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        track = models.Track.objects.filter(id=self.kwargs.get('pk1'))
        ls1 = models.Playlist(id=self.kwargs.get('pk'), user=self.request.user, title=instance.title,
                              cover=instance.cover)
        results = list(chain(instance.tracks.all(), track))
        ls1.tracks.set(results)
        ls1.save()
        return Response({'Added': self.kwargs.get('pk1')}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.tracks.remove(self.kwargs.get('pk1'))
        instance.save()
        return Response({'Deleted': self.kwargs.get('pk1')}, status=status.HTTP_200_OK)


class StreamingFileView(views.APIView):

    def set_play(self, track):
        track.plays_count += 1
        track.save()

    def get(self, request, pk):
        track = get_object_or_404(models.Track, id=pk)
        if os.path.exists(track.file.path):
            self.set_play(track)
            return FileResponse(open(track.file.path, 'rb'), filename=track.file.name)
        else:
            return Http404


class LikedSongsView(MixedSerializer, viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    # permission_classes = [IsAuthor]
    serializer_class = serializers.CreatePlayListSerializer
    serializer_classes_by_action = {
        'list': serializers.PlayListSerializer
    }

    def get_queryset(self):
        return models.Playlist.objects.filter(user=self.request.user, title='Liked songs')

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        track = models.Track.objects.filter(id=self.kwargs.get('pk'))
        pl_id = models.Playlist.objects.filter(user=self.request.user, title='Liked songs')[0].id
        ls1 = models.Playlist(id=pl_id, user=self.request.user, title=instance.title, cover=instance.cover)
        results = list(chain(instance.tracks.all(), track))
        ls1.tracks.set(results)
        ls1.save()
        return Response({'Added': self.kwargs.get('pk')}, status=status.HTTP_200_OK)

    def destroy(self, request,  *args, **kwargs):
        instance = self.get_object()
        instance.tracks.remove(self.kwargs.get('pk1'))
        instance.save()
        return Response({'Deleted': self.kwargs.get('pk1')}, status=status.HTTP_200_OK)
