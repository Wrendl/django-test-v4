from django.core.validators import FileExtensionValidator
from django.db import models
from accounts.models import UserAccount
from base.services import get_path_upload_cover_album, validate_size_image, get_path_upload_track, \
    get_path_upload_playlist, get_default_cover


class Genre(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    # user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='albums')
    user_name = models.CharField(max_length=50, default='no author')
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    private = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to=get_path_upload_cover_album,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png']), validate_size_image],
    )
    # REQUIRED_FIELDS = ['user_name', 'name', 'description']


class Track(models.Model):
    # user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre, related_name='track_genres')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True)
    file = models.FileField(
        upload_to=get_path_upload_track,
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'mp4', 'wav'])],
    )
    create_at = models.DateTimeField(auto_now_add=True)
    plays_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.title}'


class Playlist(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='playlist')
    title = models.CharField(max_length=100)
    tracks = models.ManyToManyField(Track, related_name='track_playlist', blank=True, null=True, )
    cover = models.ImageField(
        upload_to=get_path_upload_playlist,
        blank=True,
        null=True,
        default='',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png']), validate_size_image],
    )