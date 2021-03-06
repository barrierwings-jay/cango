# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 05:40
from __future__ import unicode_literals

import bfm.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bfm', '0015_auto_20170311_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='p_extra_pic6',
            field=models.ImageField(null=True, upload_to=bfm.models.Place.get_image_path),
        ),
        migrations.AddField(
            model_name='place',
            name='p_extra_pic7',
            field=models.ImageField(null=True, upload_to=bfm.models.Place.get_image_path),
        ),
        migrations.AddField(
            model_name='place',
            name='p_extra_pic8',
            field=models.ImageField(null=True, upload_to=bfm.models.Place.get_image_path),
        ),
        migrations.AlterField(
            model_name='place',
            name='p_extra_pic1',
            field=models.ImageField(null=True, upload_to=bfm.models.Place.get_image_path),
        ),
        migrations.AlterField(
            model_name='place',
            name='p_extra_pic2',
            field=models.ImageField(null=True, upload_to=bfm.models.Place.get_image_path),
        ),
        migrations.AlterField(
            model_name='place',
            name='p_extra_pic3',
            field=models.ImageField(null=True, upload_to=bfm.models.Place.get_image_path),
        ),
        migrations.AlterField(
            model_name='place',
            name='p_extra_pic4',
            field=models.ImageField(null=True, upload_to=bfm.models.Place.get_image_path),
        ),
        migrations.AlterField(
            model_name='place',
            name='p_extra_pic5',
            field=models.ImageField(null=True, upload_to=bfm.models.Place.get_image_path),
        ),
    ]
