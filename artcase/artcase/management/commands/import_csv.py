from django.core.management.base import BaseCommand, CommandError
from artcase.models import Artifact, Creator

class Command(BaseCommand):
    help = 'Imports data from a specially structured CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str)
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        self.stdout.write(
            'No items from file {} read into model {}.'.format(
                options['filename'], options['model']))