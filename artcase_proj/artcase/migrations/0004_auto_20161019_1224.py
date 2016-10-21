# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-19 12:24
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('artcase', '0003_auto_20161001_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='size_d',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='size_h',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='size_unit',
            field=models.CharField(choices=[('cm', 'centimeters'), ('in', 'inches')], default='in', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='size_w',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='subjects',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]