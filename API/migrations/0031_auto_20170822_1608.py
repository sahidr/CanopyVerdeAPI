# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-22 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0030_auto_20170822_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='images/logo.png', null=True, upload_to='images/profile/'),
        ),
    ]
