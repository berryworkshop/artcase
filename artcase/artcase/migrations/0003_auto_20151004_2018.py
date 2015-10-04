# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artcase', '0002_category_name_russian'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name_russian',
            field=models.CharField(max_length=100),
        ),
    ]
