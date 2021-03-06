# Generated by Django 4.0.3 on 2022-04-19 12:10

import base.services
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio_library', '0006_alter_playlist_tracks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='cover',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=base.services.get_path_upload_playlist, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png']), base.services.validate_size_image]),
        ),
    ]
