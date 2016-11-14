from django.test import TestCase
from artcase.models import (
    Work,
    Creator,
    Value,
    Location,
    Medium,
    Image,
    Category,
    Collection
)


class WorkTestCase(TestCase):
    fixtures = ['fixture_basic.yaml']

    def setUp(self):
        self.work_a = Work.objects.get(sku="abc-123")
        self.work_b = Work.objects.get(sku="AaBb01234")
        self.creator_a = Creator.objects.get(last_name="Smith")
        self.creator_b = Creator.objects.get(last_name="Doe")
        self.value_a = Value.objects.get(value=123.45)
        self.value_b = Value.objects.get(value=45000000)
        self.location_a = Location.objects.get(name="Home")
        self.location_b = Location.objects.get(name="Work")
        self.medium_a = Medium.objects.get(name="Oil on canvas")
        self.medium_b = Medium.objects.get(name="Acrylic on paper")
        # self.image_a = Image.objects.get()
        # self.image_b = Image.objects.get()
        self.category_a = Category.objects.get(name="Paintings")
        self.category_b = Category.objects.get(name="Drawings")
        self.collection_a = Collection.objects.get(name="Public")
        self.collection_b = Collection.objects.get(name="Private")


    # base

    def test_models_have_correct_absolute_url(self):
        '''Works return accurate absolute urls'''
        self.assertEqual(self.work_a.get_absolute_url(), '/artcase/work/1')
        self.assertEqual(self.work_b.get_absolute_url(), '/artcase/work/2')

    def test_models_have_correct_create_url(self):
        '''Works return accurate creation urls'''
        self.assertEqual(self.work_a.get_create_url(), '/artcase/work_create')
        self.assertEqual(self.work_b.get_create_url(), '/artcase/work_create')

    def test_models_have_correct_list_url(self):
        '''Works return accurate list urls'''
        self.assertEqual(self.work_a.get_list_url(), '/artcase/work_list')
        self.assertEqual(self.work_b.get_list_url(), '/artcase/work_list')

    def test_models_have_correct_update_url(self):
        '''Works return accurate update urls'''
        self.assertEqual(self.work_a.get_update_url(), '/artcase/work/1/update')
        self.assertEqual(self.work_b.get_update_url(), '/artcase/work/2/update')

    def test_models_have_correct_delete_url(self):
        '''Works return accurate delete urls'''
        self.assertEqual(self.work_a.get_delete_url(), '/artcase/work/1/delete')
        self.assertEqual(self.work_b.get_delete_url(), '/artcase/work/2/delete')

    # specific models

    def test_works_have_correct_str(self):
        '''Works return accurate string representation'''
        self.assertEqual(str(self.work_a), 'Work A')
        self.assertEqual(str(self.work_b), 'Work B')

    def test_creators_have_correct_str(self):
        '''Creators return accurate string representation'''
        self.assertEqual(str(self.creator_a), 'Smith, John')
        self.assertEqual(str(self.creator_b), 'Doe, Jane')

    def test_values_have_correct_str(self):
        '''Values return accurate string representation'''
        self.assertEqual(str(self.value_a),
            '123.45 USD (fair market: 2016-01-01)')
        self.assertEqual(str(self.value_b),
            '45000000.00 USD (replacement: 2016-01-01)')

    def test_locations_have_correct_str(self):
        '''Locations return accurate string representation'''
        self.assertEqual(str(self.location_a),
            'Home: 123 Anywhere Ln., Chicago, IL 60600')
        self.assertEqual(str(self.location_b),
            'Work: 1000 LaSalle Blvd, Suite 1234, Chicago, IL 60600')

    def test_media_have_correct_str(self):
        '''Media return accurate string representation'''
        self.assertEqual(str(self.medium_a), 'Oil on canvas')
        self.assertEqual(str(self.medium_b), 'Acrylic on paper')

    # def test_image_have_correct_str(self):
    #     '''Image return accurate string representation'''
    #     self.assertEqual(str(self.image_a), '')
    #     self.assertEqual(str(self.image_b), '')

    def test_category_have_correct_str(self):
        '''Collection return accurate string representation'''
        self.assertEqual(str(self.category_a), 'Paintings')
        self.assertEqual(str(self.category_b), 'Drawings')

    def test_collection_have_correct_str(self):
        '''Collection return accurate string representation'''
        self.assertEqual(str(self.collection_a), 'Public')
        self.assertEqual(str(self.collection_b), 'Private')