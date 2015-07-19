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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('code_number', models.SlugField(validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+$', 32), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')], verbose_name='Code Number', unique=True)),
                ('title_english_short', models.CharField(max_length=255, default='Untitled')),
                ('title_english_full', models.TextField(null=True, blank=True, max_length=1000)),
                ('title_original', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True, max_length=100000)),
                ('glavlit', models.CharField(null=True, blank=True, max_length=255)),
                ('edition_state', models.CharField(blank=True, max_length=255)),
                ('edition_size', models.IntegerField(null=True, blank=True)),
                ('public', models.BooleanField(verbose_name='Public or Private', choices=[(True, 'Public'), (False, 'Private')], default=False)),
                ('condition', models.CharField(max_length=10, blank=True, choices=[('poor', 'poor'), ('fair', 'fair'), ('good', 'good'), ('very_good', 'very good'), ('excellent', 'excellent'), ('near_mint', 'near mint'), ('mint', 'mint')])),
                ('support', models.CharField(max_length=100, blank=True, choices=[('paper', 'paper'), ('panel', 'panel'), ('canvas', 'canvas')], default='paper')),
            ],
            options={
                'ordering': ['code_number'],
            },
        ),
        migrations.CreateModel(
            name='ArtifactImage',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=100, unique=True)),
                ('role', models.CharField(max_length=10, blank=True, choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('verso', 'Verso'), ('detail', 'Detail'), ('key', 'Printer Key')])),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('artifact', models.ForeignKey(to='artcase.Artifact')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField(null=True, blank=True, max_length=10000)),
                ('image', models.CharField(null=True, blank=True, max_length=1000)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True)),
                ('name_latin_last', models.CharField(verbose_name='Last Name (Latin Alphabet)', max_length=100)),
                ('name_latin_first', models.CharField(verbose_name='First Name (Latin Alphabet)', blank=True, max_length=100)),
                ('name_cyrillic_last', models.CharField(verbose_name='Last Name (Cyrillic Alphabet)', blank=True, max_length=100)),
                ('name_cyrillic_first', models.CharField(verbose_name='First Name (Cyrillic Alphabet)', blank=True, max_length=100)),
                ('nationality', models.CharField(max_length=3, blank=True, choices=[('abk', 'Abkhazian'), ('alb', 'Albanian'), ('ara', 'Arabic'), ('arm', 'Armenian'), ('ava', 'Avaric'), ('aze', 'Azerbaijani'), ('bak', 'Bashkir'), ('bel', 'Belarusian'), ('bos', 'Bosnian'), ('bul', 'Bulgarian'), ('bua', 'Buriat'), ('che', 'Chechen'), ('chi', 'Chinese'), ('chk', 'Chukchi'), ('chv', 'Chuvash'), ('crh', 'Crimean Tatar'), ('hrv', 'Croatian'), ('cze', 'Czech'), ('dar', 'Dargwa'), ('eng', 'English'), ('myv', 'Erzya'), ('est', 'Estonian'), ('fin', 'Finnish'), ('fre', 'French'), ('ger', 'German'), ('gre', 'Greek'), ('hin', 'Hindi'), ('hun', 'Hungarian'), ('inh', 'Ingush'), ('ita', 'Italian'), ('jpn', 'Japanese'), ('xal', 'Kalmyk'), ('krc', 'Karachay-Balkar'), ('kaa', 'Karakalpak'), ('kaz', 'Kazakh'), ('kom', 'Komi'), ('kor', 'Korean'), ('kum', 'Kumyk'), ('kir', 'Kyrgyz'), ('lat', 'Latvian'), ('lez', 'Lezgian'), ('lit', 'Lithuanian'), ('mac', 'Macedonian'), ('chm', 'Mari'), ('mdf', 'Moksha'), ('nog', 'Nogai'), ('oss', 'Ossetic'), ('pol', 'Polish'), ('por', 'Portuguese'), ('pan', 'Punjabi'), ('rum', 'Romanain'), ('rus', 'Russian'), ('srp', 'Serbian'), ('slo', 'Slovakian'), ('slv', 'Slovenian'), ('spa', 'Spanish'), ('tgk', 'Tajik'), ('tat', 'Tatar'), ('tuk', 'Turkmen'), ('udm', 'Udmurt'), ('ukr', 'Ukrainian'), ('uzb', 'Uzbek'), ('sah', 'Yakut')])),
                ('year_birth', models.IntegerField(verbose_name='Year of Birth', null=True, blank=True)),
                ('year_death', models.IntegerField(verbose_name='Year of Death', null=True, blank=True)),
                ('description', models.TextField(blank=True, max_length=1000)),
            ],
            options={
                'ordering': ['name_latin_last', 'name_latin_first'],
            },
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('approx_day', models.BooleanField(default=False)),
                ('approx_month', models.BooleanField(default=False)),
                ('approx_year', models.BooleanField(default=False)),
                ('qualifier', models.CharField(max_length=11, null=True, blank=True, choices=[('created', 'created'), ('started', 'started'), ('completed', 'completed'), ('printed', 'printed'), ('published', 'published'), ('restored', 'restored')], default='created')),
                ('location', models.CharField(null=True, blank=True, max_length=100)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Medium',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, blank=True, choices=[('lithograph', 'lithograph'), ('etching', 'etching'), ('offset', 'offset'), ('lithograph_offset', 'lithograph/offset'), ('acrylic', 'acrylic paint'), ('oil', 'oil paint'), ('ink', 'ink'), ('graphite', 'graphite'), ('mixed_media', 'mixed media'), ('aquatint', 'aquatint')], default='lithograph')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'media',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(null=True, blank=True, max_length=100)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(null=True, blank=True, max_length=1000)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('height', models.DecimalField(max_digits=6, null=True, blank=True, decimal_places=3)),
                ('width', models.DecimalField(max_digits=6, null=True, blank=True, decimal_places=3)),
                ('depth', models.DecimalField(max_digits=6, null=True, blank=True, decimal_places=3)),
                ('size_type', models.CharField(max_length=6, choices=[('object', 'object'), ('frame', 'frame'), ('mat', 'mat'), ('sheet', 'sheet')], default='object')),
                ('unit', models.CharField(max_length=2, choices=[('in', 'inches'), ('ft', 'feet'), ('mm', 'millimeters'), ('cm', 'centimeters'), ('m', 'meters')], default='in')),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('value_type', models.CharField(max_length=3, choices=[('fmv', 'Fair Market'), ('rep', 'Replacement')], default='fmv')),
                ('date', models.DateField(null=True, blank=True)),
                ('value', models.DecimalField(max_digits=10, decimal_places=2)),
                ('agent', models.CharField(max_length=100, default='Bill Cellini')),
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
            field=models.ForeignKey(blank=True, to='artcase.Organization', related_name='artifacts_printed', null=True),
        ),
        migrations.AddField(
            model_name='artifact',
            name='publisher',
            field=models.ForeignKey(blank=True, to='artcase.Organization', related_name='artifacts_published', null=True),
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
