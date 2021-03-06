# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-08 22:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customUserModel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cangouser',
            name='nickname',
            field=models.CharField(max_length=16, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='cangouser',
            name='profile_pic',
            field=models.ImageField(default='user_profile/default.png', upload_to='user_picture/'),
        ),
    ]
