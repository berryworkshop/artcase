# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-22 03:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artcase', '0009_auto_20161022_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
