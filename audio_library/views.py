import os
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import render
from rest_framework import generics, parsers, viewsets, views, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from base.classes import MixedSerializer
from base.services import delete_old_file
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


class AlbumView(MixedSerializer, viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializers.CreateAlbumSerializer
    serializer_classes_by_action = {
        'list': serializers.AlbumSerializer
    }

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
        'list': serializers.PlayListSerializer
    }

    def get_queryset(self):
        return models.Playlist.objects.filter(user=self.request.user)[1:]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    # def patch(self, request, pk):
    #     testmodel_object = self.get_object(pk)
    #     serializer = TestModelSerializer(testmodel_object, data=request.data,
    #                                      partial=True)  # set partial=True to update a data partially
    #     if serializer.is_valid():
    #         serializer.save()
    # def update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     instance = self.get_object()
    #     instance.tracks += request.tracks
    #     instance.save(user=self.request.user)

    def destroy(self, request,  *args, **kwargs):
        instance = self.get_object()
        delete_old_file(instance.cover.path)
        self.perform_destroy(instance)
        return Response({"detail": "deleted"}, status=status.HTTP_200_OK)


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
        return models.Playlist.objects.filter(user=self.request.user)[:1]

    # def update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     instance = self.get_object()
    #     instance.tracks += request.tracks
    #     instance.save(user=self.request.user)

    def destroy(self, request,  *args, **kwargs):
        instance = self.get_object()
        delete_old_file(instance.cover.path)
        self.perform_destroy(instance)
        return Response({"detail": "deleted"}, status=status.HTTP_200_OK)