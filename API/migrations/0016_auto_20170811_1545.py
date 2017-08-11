# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-11 19:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0015_auto_20170811_1445'),
    ]

    operations = [
        migrations.RenameField(
            model_name='greenpoint',
            old_name='latitud',
            new_name='latitude',
        ),
        migrations.RenameField(
            model_name='greenpoint',
            old_name='longitud',
            new_name='longitude',
        ),
        migrations.AlterUniqueTogether(
            name='greenpoint',
            unique_together=set([('latitude', 'longitude')]),
        ),
    ]