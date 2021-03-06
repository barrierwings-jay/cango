# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 11:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bfm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='c_chair_movable',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='place',
            name='c_elevator_capacity',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='place',
            name='c_elevator_exist',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='place',
            name='c_handicapped_parking_lot',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='place',
            name='c_handicapped_toilet',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='place',
            name='c_parking_lot_exist',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='place',
            name='c_toilet_available',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='place',
            name='category',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='extra_info',
            field=models.TextField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='p_entrance',
            field=models.ImageField(default='user_profile/default.png', upload_to='test/'),
        ),
        migrations.AlterField(
            model_name='place',
            name='p_extra_pic1',
            field=models.ImageField(default='user_profile/default.png', upload_to='test/'),
        ),
        migrations.AlterField(
            model_name='place',
            name='p_extra_pic2',
            field=models.ImageField(default='user_profile/default.png', upload_to='test/'),
        ),
        migrations.AlterField(
            model_name='place',
            name='p_extra_pic3',
            field=models.ImageField(default='user_profile/default.png', upload_to='test/'),
        ),
        migrations.AlterField(
            model_name='place',
            name='p_extra_pic4',
            field=models.ImageField(default='user_profile/default.png', upload_to='test/'),
        ),
        migrations.AlterField(
            model_name='place',
            name='p_extra_pic5',
            field=models.ImageField(default='user_profile/default.png', upload_to='test/'),
        ),
        migrations.AlterField(
            model_name='place',
            name='p_interior',
            field=models.ImageField(default='user_profile/default.png', upload_to='test/'),
        ),
    ]
