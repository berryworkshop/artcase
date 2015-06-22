import os
from django.test import TestCase
from django.conf import settings
from artcase.models import Artifact, Creator, Medium, Size, Date, Value
from artcase.import_mappings import mappings
from artcase.management.commands.import_csv import Importer

class ImportTestCase(TestCase):

    def setUp(self):
        self.import_files_ok = [
            os.path.join(settings.BASE_DIR, # artifacts
                'artcase/tests/test_data/artifacts.csv'),
            os.path.join(settings.BASE_DIR, # creators
                'artcase/tests/test_data/artists.csv')
        ]
        self.non_file = '/abcd/efg/test.csv'
        self.bad_file = os.path.join(settings.BASE_DIR,
                'artcase/tests/test_data/bad_file.csv')

        artifacts = Artifact.objects.all()
        self.assertEqual(artifacts.count(), 0)
        artifacts_import = Importer(self.import_files_ok[0])
        artifacts_import.do_import()
        self.assertEqual(artifacts.count(), 51)

        self.artifact_PP001 = Artifact.objects.get(pk=1)
        self.artifact_PP002 = Artifact.objects.get(pk=2)
        self.artifact_PP003 = Artifact.objects.get(pk=3)
        self.artifact_PP008 = Artifact.objects.get(code_number='PP 008')
        self.artifact_PP048 = Artifact.objects.get(
            title_english='A Wounded Red Soldier Will Find A Mother')
        self.artifact_list = Artifact.objects.filter(edition_size=5000)

    def test_files_exist(self):
        """File specified in import_files should exist."""
        self.assertTrue(os.path.isfile(self.import_files_ok[0]))
        self.assertTrue(os.path.isfile(self.import_files_ok[1]))

    def test_basic_import(self):
        """
        Files should import correctly
        """
        self.assertEqual(self.artifact_PP001.code_number, 'PP 001')
        self.assertEqual(self.artifact_PP001.condition, 'Excellent')

        self.assertEqual(
            self.artifact_PP008.title_english, 'Molten Steel Down Throat')
        self.assertEqual(self.artifact_PP048.code_number, 'PP 048')
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
        When imports have related fields, they should import correctly.
        """

        creators = Creator.objects.all()
        self.assertEqual(creators.count(), 0)
        creators_import = Importer(self.import_files_ok[1])
        creators_import.do_import()
        self.assertEqual(creators.count(), 348)

        creators = Creator.objects.all()
        artifacts = Artifact.objects.all()

        c1 = Creator.objects.get(
            name_latin_last = 'Angelushev')
        self.assertEqual(c1.description, 'Bulgarian graphic artist')
        self.assertEqual(c1.name_cyrillic_last, 'Ангелушев')
        self.assertEqual(c1.name_cyrillic_first, 'Борис')

        a1 = Artifact.objects.get(code_number='PP 007')
        self.assertTrue('Apsit' in a1.description)

