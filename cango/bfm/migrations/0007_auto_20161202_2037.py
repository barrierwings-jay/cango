# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 11:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bfm', '0006_auto_20161202_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='bfm.Place'),
        ),
    ]
