import os
import re
import shutil
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
        tc = TestCase()
        try:
            tc.assertTrue(os.path.exists(self.input_path))
        except AssertionError:
            raise AssertionError('input "{}" does not exist'.format(self.input_path))
        try:
            tc.assertTrue(os.path.exists(self.output_dir))
        except AssertionError:
            raise AssertionError('output "{}" is not a directory'.format(self.output_dir))

        if os.path.isfile(self.input_path):
            self.import_image()
        elif os.path.isdir(self.input_path):
            self.import_images()


    def import_image(self):
        # ensure item exists
        # make sure file is an image
        # create destination folder if it doesn't exist already
        # copy image to destination
        # rename destination file
        print('single image')


    def import_images(self):
        # ensure item exists
        # make sure input is a directory
        # import each item in directory
        images = ['image 1', 'image 2', 'image 3']

        for img in images:
            print(img)


