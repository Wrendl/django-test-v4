# Generated by Django 4.0.3 on 2022-04-19 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio_library', '0004_alter_playlist_tracks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='tracks',
            field=models.ManyToManyField(default=None, related_name='track_playlist', to='audio_library.track'),
        ),
    ]
