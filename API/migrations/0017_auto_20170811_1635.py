# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-11 20:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0016_auto_20170811_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='images/'),
        ),
    ]
