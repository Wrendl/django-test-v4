# Generated by Django 4.0.3 on 2022-04-05 12:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_useraccount_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='date_of_birth',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 5, 12, 11, 22, 725132, tzinfo=utc)),
        ),
    ]