from django.core.management.base import BaseCommand, CommandError
from artcase.models import Artifact, Creator, Medium, Size, Date, Value
from artcase.import_mappings import mappings
from django.db.models.fields import TextField, CharField, IntegerField
from django.db.models.fields.related import ManyToManyField
import csv
import os
import datetime
import locale
from decimal import Decimal
from os.path import split
from django_date_extensions.fields import ApproximateDate

class Command(BaseCommand):
    help = 'Imports data from a specially structured CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):

        #with open(options['filename'], 'r') as f:
        #    reader = csv.reader(f)

        self.stdout.write(
            'No items from file {} imported.'.format(
                options['filename']))

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


    def do_import(self):
        # setup
        mapping = mappings.get(self.mapping_name, None)
        model = mapping['model']

        # execute
        for row in self.reader:
            # provide an instance to work with
            if model == Artifact:
                # create artifact, based on code_number if exists
                code_number = row.pop('Code Number', None)
                instance, created = model.objects.get_or_create(
                    code_number=code_number)
            else:
                instance = model.objects.create()

            # cherry-pick aggregate columns (those which don't replace values)
            for col_name in mapping['aggregate_fields']:
                col_value = row.pop(col_name, None)
                set_field(instance, col_name, col_value, mapping,
                    aggregate=True)

            # march through remaining columns
            for col_name, col_value in row.items():
                set_field(instance, col_name, col_value, mapping)

            instance.save()

def set_field(instance, col_name, col_value, mapping, aggregate=False):
    target_field = mapping['fields'].get(col_name, None)
    if col_value and target_field:
        # columns which should not be overwritten
        if aggregate:
            existing_val = getattr(instance, target_field, None)
            if existing_val:
                col_value = existing_val + "\n" + col_value

        # get type of field this will populate
        target_type = type(
            instance._meta.get_field_by_name(target_field)[0])

        if target_type in [TextField, CharField]:
            col_value = col_value.strip()

        if target_type == IntegerField:
            col_value = col_value.replace(',', '')
            col_value = col_value.replace('$', '')
            col_value = int(col_value)

        if target_type in [TextField, CharField, IntegerField]:
            setattr(instance, target_field, col_value)
        elif target_type in [ManyToManyField]:
            set_related_record(instance, target_field, col_value, col_name)
        else:
            raise ValueError(
                "target import field type '{}' does not exist.".format(target_type))

def set_related_record(instance, target_field, col_value, col_name):
    '''
    These are mostly one-off miscellaneous filters.  They have to live somewhere; might as well be here, until I figure out a better system.
    '''
    # needs to happen first
    instance.save()

    if col_name == 'Media':
        media_equivalents = {
            'Lithograph': 'lithograph',
            'Offset': 'offset',
            'Litho/Off': 'lithograph_offset',
        }
        if col_value in media_equivalents:
            col_value = media_equivalents[col_value]
        medium, created = Medium.objects.get_or_create(name=col_value)
        medium.save()
        instance.media.add(medium)

    if col_name == 'Media size':
        dimensions = col_value.split('x')
        assert(len(dimensions) == 2)
        for d in dimensions:
            d = float(d)
        size, created = Size.objects.get_or_create(
            height=dimensions[0], width=dimensions[1]
        )
        size.save()
        instance.sizes.add(size)

    if col_name == 'Print date' or col_name == 'Publish date':
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
        date_split = col_value.split('-')
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
        date.save()
        instance.dates.add(date)

    if col_name == 'Value':
        locale.setlocale(locale.LC_ALL, 'en_US')
        value = Decimal(locale.atof(col_value.strip("$")))
        instance.values.add(value)

