# Generated by Django 4.0.3 on 2022-04-19 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio_library', '0003_remove_album_user_album_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='tracks',
            field=models.ManyToManyField(null=True, related_name='track_playlist', to='audio_library.track'),
        ),
    ]
