# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-20 13:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artcase', '0007_auto_20161019_1815'),
    ]

    operations = [
        migrations.RenameField(
            model_name='creator',
            old_name='name_first',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='creator',
            old_name='name_last',
            new_name='last_name',
        ),
    ]