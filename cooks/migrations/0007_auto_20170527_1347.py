# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 10:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooks', '0006_auto_20170527_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='summary',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Summary'),
        ),
    ]
