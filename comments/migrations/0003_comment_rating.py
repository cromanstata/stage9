# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 18:10
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20170514_0429'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)], verbose_name='Rating'),
        ),
    ]
