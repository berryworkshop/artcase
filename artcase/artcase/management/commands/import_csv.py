from django.core.management.base import BaseCommand, CommandError
from artcase.models import Artifact, Creator, Medium, Size, Date, Value, Organization
from artcase.import_mappings import mappings
from django.db.models.fields import TextField, CharField, IntegerField
from django.db.models.fields.related import ManyToManyField
import csv
import os
import re
import datetime
import locale
from django.utils.text import slugify
from decimal import Decimal
from os.path import split
from django_date_extensions.fields import ApproximateDate
from django.test import TestCase


class Command(BaseCommand):
    help = 'Imports data from a specially structured CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        try:
            testy = TestCase()
            testy.assertTrue(os.path.isfile(options['filename']))
        except AssertionError:
            raise AssertionError('{} is not a file'.format(options['filename']))

        try:
            generic_importer = Importer(options['filename'])
            generic_importer.do_import()
        except:
            self.stdout.write(
                'No items from file {} imported.'.format(
                    options['filename']))
            raise

class Importer(object):
    '''
    Machinery for importing model data from csv files.
    '''

    def __init__(self, csv_filename):
        '''
        Prepare import: check resources, get everything setup.
        '''
        # make sure csv_filename exists
        file_exists = os.path.isfile(csv_filename)
        if not file_exists:
            raise ValueError(
                "File '{}' does not exist.".format(csv_filename))

        # validate the CSV, as well as possible, then break into rows
        csv_file = open(csv_filename, 'r')
        try:
            dialect = csv.Sniffer().sniff(csv_file.read(1024))
            csv_file.seek(0)
        except csv.Error:
            raise ValueError(
                "File '{}' is not valid CSV.".format(csv_file))
        self.reader = csv.DictReader(csv_file)

        # guess at initial mapping
        if 'artifact' in csv_filename.lower():
            self.mapping_name = 'artifact_primary'
        if 'artist' in csv_filename.lower():
            self.mapping_name = 'creator_primary'
        if 'publisher' in csv_filename.lower():
            self.mapping_name = 'publisher_primary'
        if 'printer' in csv_filename.lower():
            self.mapping_name = 'printer_primary'
        if 'glavlit' in csv_filename.lower():
            self.mapping_name = 'glavlit_primary'
        if 'translation' in csv_filename.lower():
            self.mapping_name = 'translations_primary'


    def do_import(self):
        # setup
        mapping = mappings.get(self.mapping_name, None)

        model = mapping['model']

        # execute
        for row in self.reader:
            completed_cols = [] # quick and dirty list to indicate which
            # columns have been dealt with in multiple-column operations


            # provide an instance to work with
            if model == Artifact:
                # create artifact, based on code_number if exists
                code_number = row.pop('Code Number', None)
                instance, created = model.objects.get_or_create(
                    code_number=code_number)
            elif model == Creator:
                name_latin_full = row.pop('Artist Name Roman', None)
                instance, created = model.objects.get_or_create(
                    name_latin_last=make_name_last(name_latin_full).strip(),
                    name_latin_first=make_name_first(name_latin_full).strip(),
                    slug=slugify(name_latin_full)
                )
            elif model == Organization:
                name = row.get('Name', None)
                loc = row.get('Location', None)
                if loc:
                    slug = slugify('{}_{}'.format(name[:50], loc[:49]))
                else:
                    slug = slugify(name)
                instance, created = model.objects.get_or_create(slug=slug[:100])
            else:
                pass

            # march through remaining columns
            for col_name, col_value in row.items():
                target_field = mapping['fields'].get(col_name, None)

                # direct mapping
                # these are the fields not marked as 'None' in the mapping.
                # 'None' fields are dealt with below in custom crosswalks.
                if col_value and target_field:
                    # get type of field this will populate
                    target_type = type(
                        instance._meta.get_field_by_name(target_field)[0])

                    # cleanup by field type
                    if target_type in [TextField, CharField]:
                        col_value = col_value.strip()
                    if target_type == IntegerField:
                        col_value = col_value.replace(',', '')
                        col_value = col_value.replace('$', '')
                        col_value = int(col_value)

                    # attempt to set the field quickly if possible
                    if col_value and target_type in [TextField,
                        CharField, IntegerField]:
                        setattr(instance, target_field, col_value)

                # custom crosswalks
                if col_value and self.mapping_name == 'artifact_primary':
                    if col_name == 'Media':
                        set_media(instance, col_value)
                    if col_name == 'Media size':
                        set_media_size(instance, col_value)
                    if col_name == 'Print date' or col_name == 'Publish date':
                        set_date(instance, col_value, col_name=col_name)
                    if col_name == 'Value':
                        set_value(instance, col_value)

                    # compound
                    cols = ['Notes', 'Todo']
                    if col_name in cols and col_name not in completed_cols:
                        set_artifact_description(instance, row)
                        completed_cols.extend(cols)

                if col_value and self.mapping_name == 'creator_primary':
                    if col_name == 'Artist Notes':
                        parse_creator_notes(instance, col_value)
                    if col_name == 'Artist Name Cyrillic':
                        set_name_cyrillic(instance, col_value)

                    # compound
                    cols = ['Artifact Number', 'Transcribed Name',
                        'Poster Notes']
                    if col_name in cols and col_name not in completed_cols:
                        set_creator_artifact(instance, row)
                        completed_cols.extend(cols)

                    cols = ['Second Artist Name Roman',
                        'Second Artist Name Cyrillic']
                    if col_name in cols and col_name not in completed_cols:
                        set_additional_creator(row)
                        completed_cols.extend(cols)

                if col_value and self.mapping_name in ['publisher_primary', 'printer_primary']:
                    if col_name == 'Description':
                        set_org_description(instance, col_value)
                    if col_name == 'Artifact Code':
                        set_org_artifact(instance, col_value, self.mapping_name)

                if col_value and self.mapping_name == 'translations_primary':
                    if col_name == 'Print Run':
                        set_trans_print_run(instance, col_value)
                    if col_name == 'Type':
                        set_media(instance, col_value)
                    if col_name == 'Condition':
                        set_condition(instance, col_value)
                    if col_name == 'Notes':
                        set_trans_notes(instance, col_value)

                # housekeeping
                if col_name not in completed_cols:
                    completed_cols.append(col_name)
                instance.save()



# # # # # # # # # # # # # # # # #
# Artifact crosswalk functions  #
# # # # # # # # # # # # # # # # #

def set_artifact_description(artifact, row):
    desc = ''
    notes = row.get('Notes', None).strip()
    todo = row.get('Todo', None).strip()
    if artifact.description:
        desc = artifact.description

    artifact.description = '\n'.join((desc, notes, todo)).strip()
    artifact.save()


def set_media(artifact, col_value):
    media_equivalents = {
        'Lithograph': 'lithograph',
        'Offset': 'offset',
        'Litho/Off': 'lithograph_offset',
    }
    if col_value in media_equivalents:
        col_value = media_equivalents[col_value]
    medium, created = Medium.objects.get_or_create(name=col_value)
    medium.save()
    artifact.media.add(medium)


def set_media_size(artifact, col_value):
    dimensions = col_value.split('x')
    assert(len(dimensions) == 2)
    for d in dimensions:
        d = float(d)
    size = Size.objects.create(
        height=dimensions[0], width=dimensions[1]
    )
    size.save()
    artifact.sizes.add(size)


def set_condition(artifact, col_value):
    condition_equivalents = {
        'Poor': 'poor',
        'Fair': 'fair',
        'Good': 'good',
        'Very Good': 'very_good',
        'Excellent': 'excellent',
        'Near Mint': 'near_mint',
        'Mint': 'mint',
    }
    if col_value in condition_equivalents:
        col_value = condition_equivalents[col_value]

    artifact.condition = col_value
    artifact.save()


def set_value(artifact, col_value):
    '''
    set related dollar values based on an artifact instance
    '''
    locale.setlocale(locale.LC_ALL, 'en_US')
    v = Decimal(locale.atof(col_value.strip("$")))
    value = Value.objects.create(value=v)
    value.save()
    artifact.values.add(value)


def set_date(artifact, col_value, **kwargs):
    #setup
    day, month, year = [False,False,False]
    approximates = {}
    abbreviations = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,  'may': 5,  'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
    }

    #circa
    if 'c.' in col_value:
        col_value = col_value.replace('c.', '')
        approximates['year'] = True

    # split into tuple
    date_split = re.split('[-/ ,]', col_value)

    try:
        # ideally, we get three values
        day, month, year = date_split
    except ValueError:
        # just two values (no day value)
        try:
            month, year = date_split
            approximates['day'] = True
            day = 1
        except ValueError:
            # just one value (no month value either)
            year = str(date_split[0])
            approximates['month'] = True
            approximates['day'] = True
            month = 1
            day = 1

    # convert into integers
    day = int(day)
    if type(month) == str:
        month = abbreviations[month.lower()]
    month = int(month)
    year = int(year)

    # deal with two digit dates
    if len(str(abs(year))) <= 2:
        year = year+1900

    tmp_date = datetime.datetime(year, month, day)
    date = Date(date=tmp_date)
    if 'day' in approximates:
        date.approx_day = True
    if 'month' in approximates:
        date.approx_month = True
    if 'year' in approximates:
        date.approx_year = True

    if kwargs.get('col_name', None):
        if 'print' in kwargs['col_name'].lower():
            date.qualifier='printed'
        if 'publish' in kwargs['col_name'].lower():
            date.qualifier='published'

    date.save()
    artifact.dates.add(date)



# # # # # # # # # # # # # # # #
# Creator crosswalk functions #
# # # # # # # # # # # # # # # #

def make_name_last(name):
    try:
        name_last, name_first = name.split(',', 1)
        return name_last.strip()
    except ValueError:
        return name

def make_name_first(name):
    try:
        name_last, name_first = name.split(',', 1)
        return name_first.strip()
    except ValueError:
        return name

def parse_creator_notes(creator, col_value):
    creator.description = col_value
    creator.save()

def set_name_cyrillic(creator, col_value):
    creator.name_cyrillic_last = make_name_last(col_value)
    creator.name_cyrillic_first = make_name_first(col_value)
    creator.save()

def set_creator_artifact(creator, row):
    code_number = row.get('Artifact Number', None).strip()
    creator_name = row.get(
        'Transcribed Name', None).strip()
    notes = row.get('Poster Notes', None).strip()
    artifact, created = Artifact.objects.get_or_create(code_number=code_number)
    if artifact.description:
        desc = artifact.description
    else:
        desc = ''
    creator_tagline = 'Artist transcribed as: {}'.format(creator_name)
    artifact.description = '\n'.join((desc, creator_tagline, notes)).strip()

    artifact.save()
    artifact.creators.add(creator)
    creator.save()

def set_additional_creator(row):
    # operations on second artist
    name_latin = row.get('Second Artist Name Roman', None).strip()
    name_cyrillic = row.get('Second Artist Name Roman', None).strip()
    code_number = row.get('Artifact Number', None).strip()

    c2, created = Creator.objects.get_or_create(
        name_latin_last=make_name_last(name_latin).strip(),
        name_latin_first=make_name_first(name_latin).strip(),
        slug=slugify(name_latin)
    )

    c2.name_cyrillic_last = make_name_last(name_cyrillic).strip()
    c2.name_cyrillic_first = make_name_last(name_cyrillic).strip()
    c2.save()

    artifact, created = Artifact.objects.get_or_create(code_number=code_number)
    artifact.creators.add(c2)
    artifact.save()


# # # # # # # # # # # # # # # # # # #
# Organization crosswalk functions  #
# # # # # # # # # # # # # # # # # # #

def set_org_description(organization, col_value):
    if organization.description:
        desc = '{}\n{}'.format(organization.description, col_value)
        organization.description = desc.strip()
    else:
        organization.description = col_value.strip()
    organization.save()

def set_org_artifact(organization, col_value, mapping_name):
    artifact, created = Artifact.objects.get_or_create(code_number=col_value)

    if 'print' in mapping_name:
        artifact.printer = organization
    elif 'publish' in mapping_name:
        artifact.publisher = organization

    organization.save()
    artifact.save()


# # # # # # # # # # # # # # # # # #
# Translation crosswalk functions #
# # # # # # # # # # # # # # # # # #

def set_trans_print_run(artifact, col_value):
    col_value = col_value.replace(',', '')
    artifact.edition_size = int(col_value)
    artifact.save()

def set_trans_notes(artifact, col_value):
    if artifact.description:
        desc = '{}\n{}'.format(artifact.description, col_value)
        artifact.description = desc.strip()
    else:
        artifact.description = col_value.strip()
    artifact.save()
