# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 14:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0007_auto_20170809_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='greenpoint',
            name='user',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='API.UserProfile'),
        ),
    ]
