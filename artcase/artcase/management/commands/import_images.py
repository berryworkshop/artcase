import os
import re
import shutil
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.test import TestCase
from artcase.models import Artifact, ArtifactImage
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
        self.image_roles = {
            'verso':'verso',
            'detail':'detail',
            'print key':'key'}

    def go(self):
        if self.input_path.is_dir():
            for item in self.input_path.iterdir():
                if item.is_file():
                    self.import_image(item)
        elif self.input_path.is_file():
            self.import_image(self.input_path)

    def import_image(self, input_file):
        '''
        main import machinery.
        '''
        # ensure item exists, is a file, and is an image
        tc = TestCase()
        suffixes = ['.jpg', '.jpeg', '.gif', '.png']
        tc.assertTrue(input_file.exists())
        tc.assertTrue(input_file.is_file())
        try:
            tc.assertTrue(input_file.suffix in suffixes)
        except AssertionError:
            raise AssertionError('{} is not an image'.format(input_file))

        # get source and target
        infile = str(input_file)
        outfile = str(self.rename_filestem(input_file.name)) + input_file.suffix
        outfile_path = str(self.output_dir / outfile)

        # get role
        role = None
        for key, value in self.image_roles.items():
            if key in input_file.name:
                role = key
                break

        # get an artifact to work with
        code_number = self.get_code_number(input_file.name)
        a, created = Artifact.objects.get_or_create(
            code_number=code_number,
            title_english_short="Lorem Ipsum",
            public=True)

        # outfile must be unique
        while ArtifactImage.objects.filter(filename=outfile).count() > 0:
            p = Path(outfile)
            p_stem = str(p.stem) + '_1'
            outfile = p_stem + p.suffix

        image = ArtifactImage.objects.create(
            artifact=a, filename=outfile)

        if role:
            image.role = role

        # copy image to destination
        shutil.copyfile(infile, outfile_path)


    def get_code_number(self, stem):
        # split up the stem
        regex = r'([a-zA-Z]*)[-_ ]*([\d]+)[a-zA-Z]?[-]?[\w -]*'
        code_prefix_raw, code_digits_raw = re.findall(regex, stem)[0]
        code_number = '{}-{}'.format(code_prefix_raw.lower(), code_digits_raw)
        return slugify(code_number)


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

        # image role replacement
        roles_to_add = []
        for key, value in self.image_roles.items():
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

