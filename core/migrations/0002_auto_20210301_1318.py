# Generated by Django 3.1.6 on 2021-03-01 12:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banktransfer',
            name='execute_datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 2, 12, 18, 45, 570364, tzinfo=utc)),
        ),
    ]
