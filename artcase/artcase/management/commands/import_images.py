import os
import re
import shutil
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.test import TestCase
from artcase.models import Artifact
from django.utils.text import slugify


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


class Importer(object):
    def __init__(self, input_path, output_dir):
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir)

    def go(self):
        if self.input_path.is_dir():
            for item in self.input_path.iterdir():
                if item.is_file():
                    self.import_image(item)
        elif self.input_path.is_file():
            self.import_image(self.input_path)

    def import_image(self, input_file):
        # ensure item exists, is a file, and is an image
        tc = TestCase()
        suffixes = ['.jpg', '.jpeg', '.gif', '.png']
        tc.assertTrue(input_file.exists())
        tc.assertTrue(input_file.is_file())
        try:
            tc.assertTrue(input_file.suffix in suffixes)
        except AssertionError:
            raise AssertionError('{} is not an image'.format(input_file))

        infile = str(input_file)
        outfile = str(self.output_dir / self.rename_filestem(input_file.name)) + input_file.suffix

        # copy image to destination
        shutil.copyfile(infile, outfile)


    def rename_filestem(self, stem):
        # split up the stem
        regex = r'([a-zA-Z]*)[-_ ]*([\d]+)([a-zA-Z]?)[-]?([\w -]*)'
        code_prefix_raw, code_digits_raw, code_suffix_raw, file_detail_raw \
            = re.findall(regex, stem)[0]

        # intial cleanup
        file_detail_raw = file_detail_raw.lower()
        strings_to_remove = ['images', 'image', 'catalog']
        for s in strings_to_remove:
            file_detail_raw = file_detail_raw.replace(s, '')

        # image roles
        image_roles = {'verso':'verso', 'detail':'detail', 'print key':'key'}
        roles_to_add = []
        for key, value in image_roles.items():
            if key in file_detail_raw:
                file_detail_raw = file_detail_raw.replace(key, '')
                roles_to_add.append(value)
        roles_to_add.sort()

        # reassemble
        new_stem = '{}-{}{}_{}_{}'.format(code_prefix_raw.lower(), code_digits_raw, code_suffix_raw.lower(), '-'.join(roles_to_add), slugify(file_detail_raw))

        # final cleanup
        new_stem = new_stem.replace('__', '_')
        new_stem = new_stem.rstrip('_')

        return new_stem

