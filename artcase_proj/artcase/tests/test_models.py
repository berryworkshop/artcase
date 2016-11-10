from django.test import TestCase
from artcase.models import (
    Work, Creator, Value, Location, Medium, Image, Category, Collection)


class WorkTestCase(TestCase):
    def setUp(self):
        Work.objects.create(
            title="Work A",
            sku="abc-123",
            )
        Work.objects.create(
            title="Work B",
            sku="AaBb01234",
            )
        Creator.objects.create(
            first_name="John",
            last_name="Smith",
            )
        Creator.objects.create(
            first_name="Jane",
            last_name="Doe",
            )
        Value.objects.create(
            value=123.45,
            value_type="fmv",
            date='2016-11-10',
            )
        Value.objects.create(
            value=45000000,
            value_type="rpv",
            date='2016-11-10',
            )
        Location.objects.create(
            name='Home',
            address='123 Anywhere Ln., Chicago, IL 60600',
            )
        Location.objects.create(
            name='Work',
            address='1000 LaSalle Blvd, Suite 1234, Chicago, IL 60600',
            )
        self.work_a = Work.objects.get(sku="abc-123")
        self.work_b = Work.objects.get(sku="AaBb01234")
        self.creator_a = Creator.objects.get(last_name="Smith")
        self.creator_b = Creator.objects.get(last_name="Doe")
        self.value_a = Value.objects.get(value=123.45)
        self.value_b = Value.objects.get(value=45000000)
        self.location_a = Location.objects.get(name="Home")
        self.location_b = Location.objects.get(name="Work")

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
        self.assertEqual(str(self.value_a), '123.45 USD (fair market: 2016-11-10)')
        self.assertEqual(str(self.value_b), '45000000.00 USD (replacement: 2016-11-10)')

    def test_locations_have_correct_str(self):
        '''Locations return accurate string representation'''
        self.assertEqual(str(self.location_a), 'Home: 123 Anywhere Ln., Chicago, IL 60600')
        self.assertEqual(str(self.location_b), 'Work: 1000 LaSalle Blvd, Suite 1234, Chicago, IL 60600')
