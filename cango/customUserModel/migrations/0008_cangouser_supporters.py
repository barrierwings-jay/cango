# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-19 02:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customUserModel', '0007_auto_20170118_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='cangouser',
            name='supporters',
            field=models.IntegerField(default=0),
        ),
    ]
