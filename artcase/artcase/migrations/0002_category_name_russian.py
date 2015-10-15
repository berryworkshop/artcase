# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artcase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_russian',
            field=models.CharField(default='untitled', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
