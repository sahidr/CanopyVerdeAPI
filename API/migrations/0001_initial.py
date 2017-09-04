# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-04 21:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('badge_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('max_points', models.IntegerField(unique=True)),
                ('min_points', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GameReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cause', models.CharField(max_length=60)),
                ('point_status', models.IntegerField()),
                ('point_date', models.DateField(auto_now_add=True)),
                ('point_value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('city', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('green_index', models.FloatField(default=0)),
                ('population_density', models.FloatField(default=0)),
                ('reported_trees', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TreePoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='images/tree/')),
                ('date', models.DateField(auto_now_add=True)),
                ('canopy', models.IntegerField(blank=True, default=0)),
                ('stem', models.IntegerField(blank=True, default=0)),
                ('height', models.IntegerField(blank=True, default=0)),
                ('type', models.CharField(blank=True, max_length=100)),
                ('location', models.CharField(max_length=255)),
                ('status', models.IntegerField()),
                ('city', models.CharField(default=None, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('fk_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('fullname', models.CharField(max_length=60)),
                ('profile_pic', models.ImageField(blank=True, default='images/logo.png', null=True, upload_to='images/profile/')),
                ('activation_key', models.CharField(blank=True, max_length=50)),
                ('photo_loaded', models.BooleanField(default=False)),
                ('country', models.CharField(max_length=120)),
                ('city', models.CharField(max_length=120)),
                ('game_points', models.IntegerField(blank=True, default=0)),
                ('badge', models.CharField(blank=True, default='Apprentice', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='treepoint',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='API.UserProfile'),
        ),
        migrations.AddField(
            model_name='gamereport',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='badge',
            unique_together=set([('max_points', 'min_points')]),
        ),
        migrations.AlterUniqueTogether(
            name='treepoint',
            unique_together=set([('latitude', 'longitude')]),
        ),
    ]
