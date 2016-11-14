from django.core.urlresolvers import reverse, resolve

from django.test import TestCase, Client
from artcase.models import (
    Work, Creator, Value, Location, Medium, Image, Category, Collection)

class BaseUrlTestCase(TestCase):
    fixtures = ['fixture_basic.yaml']

    def setUp(self):
        pass

    # base

    def test_work_urls(self):
        '''Make sure Work urls work ok.'''
        url = reverse('artcase:work_detail', args=[1])
        self.assertEqual(url, '/artcase/work/1')
        url = reverse('artcase:work_list')
        self.assertEqual(url, '/artcase/work_list')
        url = reverse('artcase:work_create')
        self.assertEqual(url, '/artcase/work_create')
        url = reverse('artcase:work_update', args=[1])
        self.assertEqual(url, '/artcase/work/1/update')
        url = reverse('artcase:work_delete', args=[1])
        self.assertEqual(url, '/artcase/work/1/delete')

    def test_creator_urls(self):
        '''Make sure Creator urls work ok.'''
        url = reverse('artcase:creator_detail', args=[1])
        self.assertEqual(url, '/artcase/creator/1')
        url = reverse('artcase:creator_list')
        self.assertEqual(url, '/artcase/creator_list')
        url = reverse('artcase:creator_create')
        self.assertEqual(url, '/artcase/creator_create')
        url = reverse('artcase:creator_update', args=[1])
        self.assertEqual(url, '/artcase/creator/1/update')
        url = reverse('artcase:creator_delete', args=[1])
        self.assertEqual(url, '/artcase/creator/1/delete')

    def test_location_urls(self):
        '''Make sure Location urls work ok.'''
        url = reverse('artcase:location_detail', args=[1])
        self.assertEqual(url, '/artcase/location/1')
        url = reverse('artcase:location_list')
        self.assertEqual(url, '/artcase/location_list')
        url = reverse('artcase:location_create')
        self.assertEqual(url, '/artcase/location_create')
        url = reverse('artcase:location_update', args=[1])
        self.assertEqual(url, '/artcase/location/1/update')
        url = reverse('artcase:location_delete', args=[1])
        self.assertEqual(url, '/artcase/location/1/delete')

    def test_image_urls(self):
        '''Make sure Image urls work ok.'''
        url = reverse('artcase:image_detail', args=[1])
        self.assertEqual(url, '/artcase/image/1')
        url = reverse('artcase:image_list')
        self.assertEqual(url, '/artcase/image_list')
        url = reverse('artcase:image_create')
        self.assertEqual(url, '/artcase/image_create')
        url = reverse('artcase:image_update', args=[1])
        self.assertEqual(url, '/artcase/image/1/update')
        url = reverse('artcase:image_delete', args=[1])
        self.assertEqual(url, '/artcase/image/1/delete')

    def test_medium_urls(self):
        '''Make sure Medium urls work ok.'''
        url = reverse('artcase:medium_detail', args=[1])
        self.assertEqual(url, '/artcase/medium/1')
        url = reverse('artcase:medium_list')
        self.assertEqual(url, '/artcase/medium_list')
        url = reverse('artcase:medium_create')
        self.assertEqual(url, '/artcase/medium_create')
        url = reverse('artcase:medium_update', args=[1])
        self.assertEqual(url, '/artcase/medium/1/update')
        url = reverse('artcase:medium_delete', args=[1])
        self.assertEqual(url, '/artcase/medium/1/delete')

    def test_category_urls(self):
        '''Make sure Category urls work ok.'''
        url = reverse('artcase:category_detail', args=[1])
        self.assertEqual(url, '/artcase/category/1')
        url = reverse('artcase:category_list')
        self.assertEqual(url, '/artcase/category_list')
        url = reverse('artcase:category_create')
        self.assertEqual(url, '/artcase/category_create')
        url = reverse('artcase:category_update', args=[1])
        self.assertEqual(url, '/artcase/category/1/update')
        url = reverse('artcase:category_delete', args=[1])
        self.assertEqual(url, '/artcase/category/1/delete')

    def test_collection_urls(self):
        '''Make sure Collection urls work ok.'''
        url = reverse('artcase:collection_detail', args=[1])
        self.assertEqual(url, '/artcase/collection/1')
        url = reverse('artcase:collection_list')
        self.assertEqual(url, '/artcase/collection_list')
        url = reverse('artcase:collection_create')
        self.assertEqual(url, '/artcase/collection_create')
        url = reverse('artcase:collection_update', args=[1])
        self.assertEqual(url, '/artcase/collection/1/update')
        url = reverse('artcase:collection_delete', args=[1])
        self.assertEqual(url, '/artcase/collection/1/delete')