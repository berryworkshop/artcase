from django.core.management.base import BaseCommand, CommandError
from artcase.models import Artifact, Creator
from artcase.import_mappings import mappings
import django.db.models.fields as django_fields
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
            # create artifact, based on code_number if exists
            code_number = row.pop('Code Number', None)
            if code_number:
                instance, created = model.objects.get_or_create(
                    code_number=code_number)
            else:
                instance = model.objects.create()

            # march through mappings
            for col_name, target_field in mapping['fields'].items():
                # find equivalent in csv
                col_value = row.pop(col_name, None)

                if col_value:
                    # initial cleanup
                    col_value = col_value.strip()

                    # type-specific cleanup and conversion
                    target_type = type(
                        model._meta.get_field_by_name(target_field)[0])
                    if target_type == django_fields.IntegerField:
                        col_value = col_value.replace(',', '')
                        col_value = col_value.replace('$', '')
                        col_value = int(col_value)

                    # some fields are aggregates, so add to end
                    if col_name in mapping['aggregate_fields']:
                        # col_name e.g. "Todo"
                        # target_field e.g. "description"
                        # col_value e.g. "Test Todo"
                        val = getattr(instance, target_field, None)
                        if val:
                            col_value = val + "\n" + col_value

                    # put it in
                    setattr(instance, target_field, col_value)

            instance.save()


