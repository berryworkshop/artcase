from django.core.management.base import BaseCommand, CommandError
from artcase.models import Artifact, Creator, Medium
from artcase.import_mappings import mappings
from django.db.models.fields import CharField, IntegerField
import csv
import os
from os.path import split

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
                set_field(instance, col_name, col_value, mapping, aggregate=True)

            # march through remaining columns
            for col_name, col_value in row.items():
                set_field(instance, col_name, col_value, mapping)

            instance.save()

def set_field(instance, col_name, col_value, mapping, aggregate=False):
    target_field = mapping['fields'].get(col_name, None)
    if col_value and target_field:
        target_type = type(
            instance._meta.get_field_by_name(target_field)[0])
        col_value = cleanup_convert(col_value, target_type)

        # columns which should not be overwritten
        if aggregate:
            existing_val = getattr(instance, target_field, None)
            if existing_val:
                col_value = existing_val + "\n" + col_value

        setattr(instance, target_field, col_value)


def cleanup_convert(val, target_type=CharField):
    # initial cleanup
    val = val.strip()

    if target_type == IntegerField:
        val = val.replace(',', '')
        val = val.replace('$', '')
        val = int(val)

    return val