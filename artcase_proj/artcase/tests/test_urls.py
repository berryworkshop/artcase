from django.core.urlresolvers import reverse

from django.test import TestCase
from artcase.models import (
    Work, Creator, Value, Location, Medium, Image, Category, Collection)

class BaseUrlTestCase(TestCase):
    fixtures = ['fixture_basic.yaml']

    def setUp(self):
        pass

    # base

    # def test_urls_reverse_correctly(self):
    #     '''URLs should reverse correctly.'''
    #     url = reverse('artcase:work_detail', args=[1988])
    #     self.assertEqual(url, '/archive/')

