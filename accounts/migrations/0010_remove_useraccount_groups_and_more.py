# Generated by Django 4.0.3 on 2022-04-07 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_useraccount_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccount',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='user_permissions',
        ),
    ]
