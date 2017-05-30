# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 14:55
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cooks', '0008_auto_20170527_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)], verbose_name='Rating')),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('rater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rater', to=settings.AUTH_USER_MODEL)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='cooks.Recipe', verbose_name='Recipe')),
            ],
            options={
                'verbose_name': 'Rating',
                'verbose_name_plural': 'Rating',
            },
        ),
    ]
