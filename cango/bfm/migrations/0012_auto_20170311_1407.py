# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-11 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bfm', '0011_auto_20161203_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='category',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]