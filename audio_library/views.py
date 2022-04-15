import os

from django.http import FileResponse, Http404
from django.shortcuts import render
from rest_framework import generics, parsers, viewsets, views, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from base.classes import MixedSerializer, Pagination
from base.services import delete_old_file
from . import models, serializers


class GenreView(generics.ListAPIView):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class AlbumView(viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializers.AlbumSerializer

    # permission_classes = [IsAuthor]

    def get_queryset(self):
        return models.Album.objects.filter()
        # return models.Album.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


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
        'list': serializers.AuthorTrackSerializer
    }

    def get_queryset(self):
        return models.Playlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


# class TrackListView(generics.ListAPIView):
#     queryset = models.Track.objects.all()
#     serializer_class = serializers.AuthorTrackSerializer
#     pagination_class = Pagination


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
