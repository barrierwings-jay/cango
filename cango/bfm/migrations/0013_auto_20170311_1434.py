# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-11 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bfm', '0012_auto_20170311_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='c_elevator_capacity',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='c_floor',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]