# Generated by Django 4.0.3 on 2022-04-30 08:56

import base.services
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio_library', '0010_remove_likedsongs_tracks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=base.services.get_path_upload_cover_album, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg']), base.services.validate_size_image]),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='cover',
            field=models.ImageField(blank=True, default='default\\default-cover.png', null=True, upload_to=base.services.get_path_upload_playlist, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg']), base.services.validate_size_image]),
        ),
        migrations.DeleteModel(
            name='LikedSongs',
        ),
    ]