# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-11 18:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0013_auto_20170809_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='greenpoint',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='API.UserProfile'),
        ),
    ]
