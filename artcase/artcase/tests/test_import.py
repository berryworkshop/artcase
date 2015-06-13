import os
from django.test import TestCase
from django.conf import settings
from artcase.models import Artifact, Creator
from artcase.import_mappings import mappings
from artcase.management.commands.import_csv import Importer

class ImportTestCase(TestCase):

    def setUp(self):
        self.import_files_ok = [
            os.path.join(settings.BASE_DIR,
                'artcase/tests/test_data/artifacts.csv'),
            os.path.join(settings.BASE_DIR,
                'artcase/tests/test_data/artists.csv')
        ]
        self.non_file = '/abcd/efg/test.csv'
        self.bad_file = os.path.join(settings.BASE_DIR,
                'artcase/tests/test_data/bad_file.csv')

    def test_files_exist(self):
        """File specified in import_files should exist."""
        self.assertTrue(os.path.isfile(self.import_files_ok[0]))
        self.assertTrue(os.path.isfile(self.import_files_ok[1]))

    def test_import_artifacts(self):
        """
        Files should import correctly
        """
        artifacts_import = Importer(self.import_files_ok[0])

        artifacts = Artifact.objects.all()
        self.assertEqual(artifacts.count(), 0)

        artifacts_import.do_import()
        self.assertEqual(artifacts.count(), 51)

        a1 = Artifact.objects.get(pk=1)
        a2 = Artifact.objects.get(pk=2)
        a3 = Artifact.objects.get(pk=3)
        a8 = Artifact.objects.get(code_number='PP 008')
        a48 = Artifact.objects.get(title_english='A Wounded Red Soldier Will Find A Mother')
        a_list = Artifact.objects.filter(edition_size=5000)

        self.assertEqual(a1.code_number, 'PP 001')
        self.assertEqual(a1.condition, 'Excellent')
        self.assertEqual(a1.description, 'Test Notes\nTest Todo')

        self.assertEqual(a2.description, 'Test Notes')
        self.assertEqual(a3.description, 'Test Todo')

        self.assertEqual(a8.title_english, 'Molten Steel Down Throat')
        self.assertEqual(a48.code_number, 'PP 048')
        self.assertEqual(a48.condition, 'Very Good')
        self.assertEqual(a_list.count(), 3)




