# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import re


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artifact',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('code_number', models.SlugField(validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+$', 32), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')], unique=True, verbose_name='Code Number')),
                ('title_english_short', models.CharField(default='Untitled', null=True, max_length=255, blank=True)),
                ('title_english_full', models.TextField(null=True, max_length=1000, blank=True)),
                ('title_original', models.CharField(max_length=255, blank=True)),
                ('description', models.TextField(max_length=100000, blank=True)),
                ('glavlit', models.CharField(null=True, max_length=255, blank=True)),
                ('edition_state', models.CharField(null=True, max_length=255, blank=True)),
                ('edition_size', models.IntegerField(null=True, blank=True)),
                ('public', models.BooleanField(choices=[(True, 'Public'), (False, 'Private')], default=False, verbose_name='Public or Private')),
                ('condition', models.CharField(choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('very_good', 'very good'), ('excellent', 'excellent'), ('near_mint', 'near mint'), ('mint', 'mint')], max_length=10, blank=True)),
                ('support', models.CharField(default='paper', choices=[('paper', 'paper'), ('panel', 'panel'), ('canvas', 'canvas')], max_length=100, blank=True)),
            ],
            options={
                'ordering': ['code_number'],
            },
        ),
        migrations.CreateModel(
            name='ArtifactImage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('filename', models.CharField(unique=True, max_length=100)),
                ('role', models.CharField(choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('verso', 'Verso'), ('detail', 'Detail'), ('key', 'Printer Key')], max_length=10, blank=True)),
                ('description', models.TextField(max_length=1000, blank=True)),
                ('artifact', models.ForeignKey(to='artcase.Artifact')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('description', models.TextField(null=True, max_length=10000, blank=True)),
                ('image', models.CharField(null=True, max_length=1000, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('slug', models.SlugField(unique=True)),
                ('name_latin_last', models.CharField(max_length=100, verbose_name='Last Name (Latin Alphabet)')),
                ('name_latin_first', models.CharField(max_length=100, verbose_name='First Name (Latin Alphabet)', blank=True)),
                ('name_cyrillic_last', models.CharField(max_length=100, verbose_name='Last Name (Cyrillic Alphabet)', blank=True)),
                ('name_cyrillic_first', models.CharField(max_length=100, verbose_name='First Name (Cyrillic Alphabet)', blank=True)),
                ('nationality', models.CharField(choices=[('abk', 'Abkhazian'), ('alb', 'Albanian'), ('ara', 'Arabic'), ('arm', 'Armenian'), ('ava', 'Avaric'), ('aze', 'Azerbaijani'), ('bak', 'Bashkir'), ('bel', 'Belarusian'), ('bos', 'Bosnian'), ('bul', 'Bulgarian'), ('bua', 'Buriat'), ('che', 'Chechen'), ('chi', 'Chinese'), ('chk', 'Chukchi'), ('chv', 'Chuvash'), ('crh', 'Crimean Tatar'), ('hrv', 'Croatian'), ('cze', 'Czech'), ('dar', 'Dargwa'), ('eng', 'English'), ('myv', 'Erzya'), ('est', 'Estonian'), ('fin', 'Finnish'), ('fre', 'French'), ('ger', 'German'), ('gre', 'Greek'), ('hin', 'Hindi'), ('hun', 'Hungarian'), ('inh', 'Ingush'), ('ita', 'Italian'), ('jpn', 'Japanese'), ('xal', 'Kalmyk'), ('krc', 'Karachay-Balkar'), ('kaa', 'Karakalpak'), ('kaz', 'Kazakh'), ('kom', 'Komi'), ('kor', 'Korean'), ('kum', 'Kumyk'), ('kir', 'Kyrgyz'), ('lat', 'Latvian'), ('lez', 'Lezgian'), ('lit', 'Lithuanian'), ('mac', 'Macedonian'), ('chm', 'Mari'), ('mdf', 'Moksha'), ('nog', 'Nogai'), ('oss', 'Ossetic'), ('pol', 'Polish'), ('por', 'Portuguese'), ('pan', 'Punjabi'), ('rum', 'Romanain'), ('rus', 'Russian'), ('srp', 'Serbian'), ('slo', 'Slovakian'), ('slv', 'Slovenian'), ('spa', 'Spanish'), ('tgk', 'Tajik'), ('tat', 'Tatar'), ('tuk', 'Turkmen'), ('udm', 'Udmurt'), ('ukr', 'Ukrainian'), ('uzb', 'Uzbek'), ('sah', 'Yakut')], max_length=3, blank=True)),
                ('year_birth', models.IntegerField(null=True, verbose_name='Year of Birth', blank=True)),
                ('year_death', models.IntegerField(null=True, verbose_name='Year of Death', blank=True)),
                ('description', models.TextField(max_length=1000, blank=True)),
            ],
            options={
                'ordering': ['name_latin_last', 'name_latin_first'],
            },
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date', models.DateField()),
                ('approx_day', models.BooleanField(default=False)),
                ('approx_month', models.BooleanField(default=False)),
                ('approx_year', models.BooleanField(default=False)),
                ('qualifier', models.CharField(default='created', choices=[('created', 'created'), ('started', 'started'), ('completed', 'completed'), ('printed', 'printed'), ('published', 'published'), ('restored', 'restored')], max_length=11, null=True, blank=True)),
                ('location', models.CharField(null=True, max_length=100, blank=True)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Medium',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(default='lithograph', choices=[('lithograph', 'lithograph'), ('etching', 'etching'), ('offset', 'offset'), ('lithograph_offset', 'lithograph/offset'), ('acrylic', 'acrylic paint'), ('oil', 'oil paint'), ('ink', 'ink'), ('graphite', 'graphite'), ('mixed_media', 'mixed media'), ('aquatint', 'aquatint')], max_length=10, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'media',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(null=True, max_length=100, blank=True)),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('description', models.TextField(null=True, max_length=1000, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('height', models.DecimalField(null=True, decimal_places=3, blank=True, max_digits=6)),
                ('width', models.DecimalField(null=True, decimal_places=3, blank=True, max_digits=6)),
                ('depth', models.DecimalField(null=True, decimal_places=3, blank=True, max_digits=6)),
                ('size_type', models.CharField(default='object', choices=[('object', 'object'), ('frame', 'frame'), ('mat', 'mat'), ('sheet', 'sheet')], max_length=6)),
                ('unit', models.CharField(default='in', choices=[('in', 'inches'), ('ft', 'feet'), ('mm', 'millimeters'), ('cm', 'centimeters'), ('m', 'meters')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('value_type', models.CharField(default='fmv', choices=[('fmv', 'Fair Market'), ('rep', 'Replacement')], max_length=3)),
                ('date', models.DateField(null=True, blank=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('agent', models.CharField(default='Bill Cellini', max_length=100)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='creator',
            unique_together=set([('name_latin_last', 'name_latin_first')]),
        ),
        migrations.AddField(
            model_name='artifact',
            name='categories',
            field=models.ManyToManyField(to='artcase.Category', blank=True),
        ),
        migrations.AddField(
            model_name='artifact',
            name='creators',
            field=models.ManyToManyField(to='artcase.Creator', blank=True),
        ),
        migrations.AddField(
            model_name='artifact',
            name='dates',
            field=models.ManyToManyField(to='artcase.Date', blank=True),
        ),
        migrations.AddField(
            model_name='artifact',
            name='media',
            field=models.ManyToManyField(to='artcase.Medium', blank=True),
        ),
        migrations.AddField(
            model_name='artifact',
            name='printer',
            field=models.ForeignKey(to='artcase.Organization', related_name='artifacts_printed', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='artifact',
            name='publisher',
            field=models.ForeignKey(to='artcase.Organization', related_name='artifacts_published', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='artifact',
            name='sizes',
            field=models.ManyToManyField(to='artcase.Size', blank=True),
        ),
        migrations.AddField(
            model_name='artifact',
            name='values',
            field=models.ManyToManyField(to='artcase.Value', blank=True),
        ),
    ]
