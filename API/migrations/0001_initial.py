# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 13:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GreenPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('image', models.URLField(blank=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('canopy', models.IntegerField()),
                ('stem', models.IntegerField()),
                ('height', models.IntegerField()),
                ('type', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=255)),
                ('status', models.IntegerField()),
                ('user', models.EmailField(max_length=254)),
            ],
        ),
    ]
