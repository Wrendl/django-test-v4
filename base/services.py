import os
import shutil

from django.core.exceptions import ValidationError

from auth_system.settings import MEDIA_ROOT


def get_path_upload_avatar(instance, file):
    """
    path to avatar, format: (media)/avatar/user_id/photo.jpg
    """
    return f'avatar/{instance.id}/{file}'


def get_path_upload_cover_album(instance, file):
    """
    path to avatar, format: (media)/album/user_id/photo.jpg
    """
    return f'album/user_{instance.user_name}/{file}'


def get_path_upload_track(instance, file):
    """
    path to avatar, format: (media)/track/user_id/photo.jpg
    """
    return f'track/title_{instance.title}/{file}'


def get_path_upload_playlist(instance, file):
    """
    path to avatar, format: (media)/playlist/user_id/photo.jpg
    """
    return f'playlist/user_{instance.user.id}/{file}'


def validate_size_image(file_obj):
    """
    Check file size
    """
    megabyte_limit = 2
    if file_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Максимальный размер файла {megabyte_limit}MB")


def delete_old_file(path_file):
    if os.path.exists(path_file):
        os.remove(path_file)


def get_default_avatar():
    return ''
    # src = os.path.join(MEDIA_ROOT, 'default\\default-user-image.png')
    # dst = os.path.join(MEDIA_ROOT, 'default\\default-user-image.png')
    # shutil.copy(src, dst)
    # default_avatar
    # return default_avatar


def get_default_cover(instance):
    default_cover = os.path.join(MEDIA_ROOT, 'default\\default-user-image.png')
    return default_cover
