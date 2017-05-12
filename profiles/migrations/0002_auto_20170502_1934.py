# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-02 16:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='city',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='organization',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='photo',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='website',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterModelTable(
            name='userprofile',
            table=None,
        ),
    ]