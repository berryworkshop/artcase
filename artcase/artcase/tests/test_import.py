import os
import tempfile
import random
import string
from pathlib import Path
from django.test import TestCase
from django.conf import settings
from artcase.models import Artifact, Creator, Medium, Size, Date, Value, Organization
from artcase.import_mappings import mappings
from artcase.management.commands import import_csv, import_images

class ImportCSVTestCase(TestCase):
    def setUp(self):
        self.import_files_ok = {
            'artifacts': os.path.join(settings.BASE_DIR, # artifacts
                'artcase/tests/test_data/artifacts.csv'),
            'creators': os.path.join(settings.BASE_DIR, # creators
                'artcase/tests/test_data/artists.csv'),
            'publishers': os.path.join(settings.BASE_DIR, # publishers
                'artcase/tests/test_data/publishers.csv'),
            'printers': os.path.join(settings.BASE_DIR, # printers
                'artcase/tests/test_data/printers.csv'),
            'glavlit': os.path.join(settings.BASE_DIR, # glavlit directory
                'artcase/tests/test_data/glavlit.csv'),
            'translations': os.path.join(settings.BASE_DIR, # translations
                'artcase/tests/test_data/translations.csv')
        }
        self.non_file = '/abcd/efg/test.csv'
        self.bad_file = os.path.join(settings.BASE_DIR,
                'artcase/tests/test_data/bad_file.csv')

        artifacts = Artifact.objects.all()
        self.assertEqual(artifacts.count(), 0)
        artifacts_import = import_csv.Importer(self.import_files_ok['artifacts'])
        artifacts_import.do_import()
        self.assertEqual(artifacts.count(), 51)

        self.artifact_PP001 = Artifact.objects.get(pk=1)
        self.artifact_PP002 = Artifact.objects.get(pk=2)
        self.artifact_PP003 = Artifact.objects.get(pk=3)
        self.artifact_PP008 = Artifact.objects.get(code_number='pp-008')
        self.artifact_PP048 = Artifact.objects.get(
            title_english_short='A Wounded Red Soldier Will Find A Mother')
        self.artifact_list = Artifact.objects.filter(edition_size=5000)

    def test_files_exist(self):
        """File specified in import_files should exist."""
        for key, value in self.import_files_ok.items():
            try:
                self.assertTrue(os.path.isfile(value))
            except AssertionError:
                raise AssertionError('{} is not a file'.format(value))

    def test_basic_import(self):
        """
        Files should import correctly
        """
        self.assertEqual(self.artifact_PP001.code_number, 'pp-001')
        self.assertEqual(self.artifact_PP001.condition, 'Excellent')

        self.assertEqual(
            self.artifact_PP008.title_english_short, 'Molten Steel Down Throat')
        self.assertEqual(self.artifact_PP048.code_number, 'pp-048')
        self.assertEqual(self.artifact_PP048.condition, 'Very Good')
        self.assertEqual(self.artifact_list.count(), 3)

    def test_import_aggregates(self):
        """
        When imports have aggregate fields, that is, fields which do not obliterate existing metadata, they should be correctly concatenated.
        """
        self.assertEqual(self.artifact_PP002.description, 'Test Notes')
        self.assertEqual(self.artifact_PP003.description, 'Test Todo')
        self.assertEqual(self.artifact_PP001.description, 'Test Notes\nTest Todo')

    def test_import_related(self):
        """
        When imports have related fields, they should import correctly.
        """
        media = Medium.objects.all()
        self.assertEqual(media.count(), 3)

        lithographs = Medium.objects.filter(name='lithograph')
        self.assertEqual(lithographs.count(), 1)

        bad_lithographs = Medium.objects.filter(name='Litho/Off')
        self.assertFalse(bad_lithographs.exists())

        sizes = Size.objects.all()
        self.assertEqual(sizes.count(), 51)

        dates = Date.objects.all()
        self.assertEqual(dates.count(), 66)

        dates_1939 = Date.objects.filter(date__year=1939)
        self.assertEqual(dates_1939.count(), 4)

        date_1 = Date.objects.get(date__year=1932, date__month=8)
        date_2 = Date.objects.get(date__year=1956, date__month=7)
        date_3 = Date.objects.get(date__year=1944)
        self.assertEqual(date_1.__str__(), 'printed: August 1932')
        self.assertEqual(date_2.__str__(), 'printed: 18 July 1956')
        self.assertEqual(date_3.__str__(), 'published: c.1944')

        values = Value.objects.all()
        self.assertEqual(values.count(), 51)

    def test_import_creators(self):
        """
        Creators should import properly.
        """

        creators = Creator.objects.all()
        self.assertEqual(creators.count(), 0)
        creators_import = import_csv.Importer(self.import_files_ok['creators'])
        creators_import.do_import()
        self.assertEqual(creators.count(), 347)

        creators = Creator.objects.all()
        artifacts = Artifact.objects.all()

        c1 = Creator.objects.get(
            name_latin_last = 'Angelushev')
        self.assertEqual(c1.description, 'Bulgarian graphic artist')
        self.assertEqual(c1.name_cyrillic_last, 'Ангелушев')
        self.assertEqual(c1.name_cyrillic_first, 'Борис')

        a1 = Artifact.objects.get(code_number='pp-007')
        self.assertTrue('Apsit' in a1.description)

        creators_no_slug = Creator.objects.filter(slug='')
        self.assertEqual(creators_no_slug.count(), 0)

    def test_import_orgs(self):
        """
        Organizations (publishers and printers) should import properly.
        """
        orgs = Organization.objects.all()
        self.assertEqual(orgs.count(), 0)
        publishers_import = import_csv.Importer(self.import_files_ok['publishers'])
        publishers_import.do_import()
        self.assertEqual(orgs.count(), 246)

        printers_import = import_csv.Importer(self.import_files_ok['printers'])
        printers_import.do_import()

        self.assertEqual(orgs.count(), 606)

        artifacts_with_publishers = Artifact.objects.filter(publisher__isnull=False)
        publishers = Organization.objects.filter(
            artifacts_published__in=artifacts_with_publishers).distinct()
        self.assertEqual(publishers.count(), 246)

        artifacts_with_printers = Artifact.objects.filter(printer__isnull=False)
        printers = Organization.objects.filter(
            artifacts_printed__in=artifacts_with_printers).distinct()
        self.assertEqual(printers.count(), 365)

        orgs_no_slug = Organization.objects.filter(slug='')
        self.assertEqual(orgs_no_slug.count(), 0)

    def test_import_glavlit(self):
        artifacts_with_glavlit = Artifact.objects.filter(glavlit__isnull=False)
        self.assertEqual(artifacts_with_glavlit.count(), 0)

        glavlit_import = import_csv.Importer(self.import_files_ok['glavlit'])
        glavlit_import.do_import()
        self.assertEqual(artifacts_with_glavlit.count(), 132)

    def test_import_translations(self):
        artifacts_with_title_full = Artifact.objects.filter(title_english_full__isnull=False)
        self.assertEqual(artifacts_with_title_full.count(), 0)

        translation_import = import_csv.Importer(self.import_files_ok['translations'])
        translation_import.do_import()

        self.assertEqual(artifacts_with_title_full.count(), 51)

        a1 = Artifact.objects.get(code_number='pp-029')
        self.assertEqual(a1.title_english_full, 'Kerenshina [government under Kerenskii]')
        self.assertEqual(a1.edition_size, 50000)
        self.assertEqual(a1.condition, 'very_good')

class ImportImagesTestCase(TestCase):
    def setUp(self):
        #./manage.py import_images ~/Desktop/cellini_photos/PP\ 048\ Catalog\ Image.jpg --settings=core.settings.local
        #./manage.py import_images ~/Desktop/cellini_photos/ --settings=core.settings.local

        # specify source files/directories to import
        self.image_source_dir = os.path.join(settings.TEST_DATA, 'images')
        self.image_filename_1 = 'PP 007 Catalog Image detail.jpg'

        # create a temporary destination directory
        self.tmp_dest_dir = os.path.join(tempfile.gettempdir(), 'django_test', ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)]))

        # basic assertions to make sure shit is OK
        self.assertFalse(os.path.exists(self.tmp_dest_dir))
        self.assertTrue(os.path.exists(self.image_source_dir))

        os.makedirs(self.tmp_dest_dir, exist_ok=True)
        self.assertTrue(os.path.exists(self.tmp_dest_dir))

        # more specific assertions about known data in source folder
        self.assertEqual(len(os.listdir(self.image_source_dir)), 19)
        self.assertTrue(os.path.exists(
            os.path.join(self.image_source_dir, self.image_filename_1)))


    def test_import_images(self):
        test_dir = Path(self.image_source_dir)
        test_img = Path(self.image_source_dir) / self.image_filename_1

        dest_directory = Path(self.tmp_dest_dir)
        self.assertTrue(dest_directory.exists())

        importer_1 = import_images.Importer(test_img, dest_directory)
        importer_1.go()

        importer_2 = import_images.Importer(test_dir, dest_directory)
        importer_2.go()

        self.assertEqual(len(os.listdir(self.tmp_dest_dir)), 19)

        img_in_1 = Path(self.image_source_dir) / 'PP 007 Catalog Image detail.jpg'
        img_out_1 = Path(dest_directory) / 'pp-007_detail.jpg'

        self.assertTrue(img_in_1.exists())
        self.assertTrue(img_out_1.exists())



