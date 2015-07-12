import os
import re
import shutil
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.test import TestCase
from artcase.models import Artifact


class Command(BaseCommand):
    help = 'Imports images, either singly, or as a folder.'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        try:
            testy = TestCase()
            testy.assertTrue(os.path.exists(options['path']))
        except AssertionError:
            raise AssertionError('{} does not exist'.format(options['path']))

        # get input; can be an image or a directory of images
        input_path = options['path']

        # specify output target directory
        self.output_directory = os.path.join(
            settings.MEDIA_ROOT, 'pictures/artifacts/')

        importer = Importer(input_path, output_directory)

        # assemble input into a list of files
        # if os.path.isfile(input_path):
        #     self.import_image(input_path, output_directory)
        # if os.path.isdir(input_path):
        #     self.import_images(input_path, output_directory)


class Importer(object):
    def __init__(self, input_path, output_dir):
        self.input_path = input_path
        self.output_dir = output_dir

    def go(self):
        p = Path(self.input_path)
        if p.is_dir():
            for item in p.iterdir():
                if item.is_file():
                    self.import_image(item)
        elif p.is_file():
            self.import_image(p)


    def import_image(self, input_file):
        # ensure item exists
        # make sure file is an image
        # create destination folder if it doesn't exist already
        # copy image to destination
        # rename destination file
        print('{}'.format(input_file))




