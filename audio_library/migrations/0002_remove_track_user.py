# Generated by Django 4.0.3 on 2022-04-13 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('audio_library', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='user',
        ),
    ]
