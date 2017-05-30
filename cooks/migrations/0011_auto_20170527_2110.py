# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 18:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_comment_rating'),
        ('cooks', '0010_rating_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='comment',
        ),
        migrations.AddField(
            model_name='rating',
            name='comment_key',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='rating4cooks', to='comments.Comment', verbose_name='Comment'),
            preserve_default=False,
        ),
    ]
