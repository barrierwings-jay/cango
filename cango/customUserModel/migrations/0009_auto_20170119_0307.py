# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-19 03:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customUserModel', '0008_cangouser_supporters'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='cangouser',
            table='cango_user',
        ),
    ]